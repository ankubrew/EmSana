from typing import List, Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime
from passlib.context import CryptContext

# Шифрование паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


#  НАСТРОЙКА БАЗЫ ДАННЫХ
sqlite_file_name = "emsana.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ТАБЛИЦЫ (МОДЕЛИ)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # unique=True означает: "В базе не может быть двух одинаковых ИИН"
    iin: str = Field(unique=True)  # БЫЛО inn, СТАЛО iin
    first_name: str
    last_name: str
    role: str
    doctor_id: Optional[int] = Field(default=None)
    password: str

class DailyLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int
    temperature: float
    symptoms: str
    photo_base64: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class Medication(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int
    name: str
    time: str
    is_taken: bool = False

# ЭНДПОИНТЫ (API) 

@app.get("/")
def read_root():
    return {"message": "Сервер EmSana работает!"}

# --- Регистрация / Создание юзера ---
@app.post("/users/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    user.password = get_password_hash(user.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# --- Получение юзера ---
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# --- Добавить запись в дневник ---
@app.post("/logs/add", response_model=DailyLog)
def add_daily_log(log: DailyLog, session: Session = Depends(get_session)):
    session.add(log)
    session.commit()
    session.refresh(log)
    return log

# --- Врач: Список своих пациентов ---
@app.get("/doctor/{doctor_id}/patients", response_model=List[User])
def get_my_patients(doctor_id: int, session: Session = Depends(get_session)):
    statement = select(User).where(User.doctor_id == doctor_id)
    results = session.exec(statement)
    return results.all()

# --- Врач: История болезни пациента ---
@app.get("/doctor/patient-history/{patient_id}", response_model=List[DailyLog])
def get_patient_history(patient_id: int, session: Session = Depends(get_session)):
    statement = select(DailyLog).where(DailyLog.patient_id == patient_id)
    results = session.exec(statement)
    return results.all()

# --- Назначить лекарство ---
@app.post("/medications/add", response_model=Medication)
def add_medication(med: Medication, session: Session = Depends(get_session)):
    session.add(med)
    session.commit()
    session.refresh(med)
    return med

# Создаем модель данных специально для входа (Login)
class LoginRequest(SQLModel):
    iin: str   # БЫЛО inn, СТАЛО iin
    password: str

@app.post("/login")
def login(request: LoginRequest, session: Session = Depends(get_session)):
    # 1. Ищем человека по ИИН
    statement = select(User).where(User.iin == request.iin) # БЫЛО inn, СТАЛО iin
    user = session.exec(statement).first()
    
    # 2. Если такого нет ИЛИ пароль не подходит
    if not user or not verify_password(request.password, user.password):
        return {"status": "error", "message": "Неверный логин или пароль"}
    
    # 3. Если всё ок
    return {
        "status": "success", 
        "user_id": user.id, 
        "role": user.role,
        "first_name": user.first_name
    }

# --- Пациент: Мои лекарства ---
@app.get("/medications/{patient_id}", response_model=List[Medication])
def get_patient_meds(patient_id: int, session: Session = Depends(get_session)):
    statement = select(Medication).where(Medication.patient_id == patient_id)
    results = session.exec(statement)
    return results.all()


#запуск
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)