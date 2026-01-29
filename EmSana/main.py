from typing import List, Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
import uvicorn # Импорт нужен для запуска внутри скрипта

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

# НАСТРОЙКА CORS (ЧТОБЫ ДРУГ МОГ ПОДКЛЮЧИТЬСЯ)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- ТАБЛИЦЫ (МОДЕЛИ) ---

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True) # ДОБАВИЛИ EMAIL
    iin: str = Field(unique=True)
    first_name: str
    last_name: str
    role: str # "doctor" или "patient"
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

# --- МОДЕЛЬ ДЛЯ ВХОДА (LOGIN) ---
class LoginRequest(SQLModel):
    email: str     # ТЕПЕРЬ ВХОД ПО EMAIL
    password: str

# --- ЭНДПОИНТЫ API --- 

@app.get("/")
def read_root():
    return {"message": "Сервер EmSana работает!"}

# 1. Регистрация
@app.post("/users/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    # Проверяем, нет ли уже такого email или ИИН
    existing_user = session.exec(select(User).where((User.email == user.email) | (User.iin == user.iin))).first()
    if existing_user:
         raise HTTPException(status_code=400, detail="Пользователь с таким Email или ИИН уже существует")
    
    user.password = get_password_hash(user.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# 2. Логин (Вход)
@app.post("/login")
def login(request: LoginRequest, session: Session = Depends(get_session)):
    # Ищем по EMAIL
    statement = select(User).where(User.email == request.email)
    user = session.exec(statement).first()
    
    if not user or not verify_password(request.password, user.password):
        return {"status": "error", "message": "Неверный email или пароль"}
    
    return {
        "status": "success", 
        "user_id": user.id, 
        "role": user.role,
        "first_name": user.first_name,
        "email": user.email
    }

# Остальные эндпоинты без изменений...
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/logs/add", response_model=DailyLog)
def add_daily_log(log: DailyLog, session: Session = Depends(get_session)):
    session.add(log)
    session.commit()
    session.refresh(log)
    return log

@app.get("/doctor/{doctor_id}/patients", response_model=List[User])
def get_my_patients(doctor_id: int, session: Session = Depends(get_session)):
    statement = select(User).where(User.doctor_id == doctor_id)
    results = session.exec(statement)
    return results.all()

@app.get("/doctor/patient-history/{patient_id}", response_model=List[DailyLog])
def get_patient_history(patient_id: int, session: Session = Depends(get_session)):
    statement = select(DailyLog).where(DailyLog.patient_id == patient_id)
    results = session.exec(statement)
    return results.all()

@app.post("/medications/add", response_model=Medication)
def add_medication(med: Medication, session: Session = Depends(get_session)):
    session.add(med)
    session.commit()
    session.refresh(med)
    return med

@app.get("/medications/{patient_id}", response_model=List[Medication])
def get_patient_meds(patient_id: int, session: Session = Depends(get_session)):
    statement = select(Medication).where(Medication.patient_id == patient_id)
    results = session.exec(statement)
    return results.all()

if __name__ == "__main__":
    # ВАЖНО: host="0.0.0.0" открывает доступ по сети
    uvicorn.run(app, host="0.0.0.0", port=8000)