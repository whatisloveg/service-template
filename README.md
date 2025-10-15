# 🚀 FastAPI Service Template

Шаблон для быстрого создания микросервисов на FastAPI

## Установка

**Windows:**
```powershell
irm https://raw.githubusercontent.com/whatisloveg/service-template/master/install.ps1 | iex
```

**Mac/Linux:**
```bash
curl -sSL https://raw.githubusercontent.com/whatisloveg/service-template/master/install.sh | bash
```

## Настройка

1. Создайте `.env` в корне проекта (скопируйте из `src/.env.example`)
2. Заполните необходимые переменные:
```env
SERVICE_NAME=my-service
DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=password
```

## Запуск
```bash
# Активируйте окружение
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Запустите
cd src
uvicorn app.web_app:app --port 8001
```

## Особенности

✅ FastAPI + Pydantic  
✅ PostgreSQL + Alembic  
✅ RabbitMQ (опционально)  
✅ Redis (опционально)  
✅ Loki logging (опционально)