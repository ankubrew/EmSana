# EmSana: запуск проекта (backend + frontend)

## Быстрый старт для разработки

1. **Установите зависимости**

### Backend
```bash
cd backend
python -m pip install fastapi uvicorn sqlmodel passlib[bcrypt]
```

### Frontend
```bash
cd ../frontend
npm install
```

2. **Запустите backend**
```bash
cd ../backend
python main.py
```

3. **Запустите frontend (в новом терминале)**
```bash
cd frontend
npm run dev
```

- Backend будет доступен на: http://localhost:8000
- Frontend (React) — на: http://localhost:5173
- Все запросы с фронта к API автоматически проксируются на backend (см. vite.config.js). CORS открыт для удобства разработки.

---

## Один сервер (собранный фронт + backend)

1. **Соберите фронтенд**
```bash
cd frontend
npm run build
```

2. **Запустите backend, он сам отдаст собранный фронт**
```bash
cd ../backend
python main.py
```

- Всё доступно на http://localhost:8000: API и SPA раздаются одним сервером без CORS.
- Backend отдаёт файлы из `frontend/dist` и подставляет `index.html` для всех маршрутов React (чтобы работали прямые переходы /login, /signup).

---

## Примечания
- Для работы CORS и прокси в dev ничего дополнительно настраивать не нужно.
- Если меняете API-роуты, обновите прокси в `frontend/vite.config.js`.
- Для продакшена рекомендуется запускать backend через uvicorn/gunicorn с параметрами `--host 0.0.0.0 --port 8000`.

---

## Пример .env (если потребуется)

```
# backend/.env
DATABASE_URL=sqlite:///emsana.db
```

---

## Контакты и поддержка
- Вопросы: issues на GitHub или напрямую разработчику.