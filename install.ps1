$SERVICE_NAME = Read-Host "Введите имя сервиса"
Write-Host "🚀 Создаю $SERVICE_NAME..." -ForegroundColor Green

npx degit whatisloveg/service-template $SERVICE_NAME
cd $SERVICE_NAME

# Проверяем структуру и копируем .env
if (Test-Path "src/.env.example") {
    Copy-Item src/.env.example src/.env
    Write-Host "✓ .env создан" -ForegroundColor Green
} elseif (Test-Path ".env.example") {
    Copy-Item .env.example src/.env
    Write-Host "✓ .env создан" -ForegroundColor Green
}

# Заменяем имя сервиса
if (Test-Path "src/.env") {
    (Get-Content src/.env) -replace 'template-service', $SERVICE_NAME | Set-Content src/.env
    Write-Host "✓ Имя сервиса обновлено" -ForegroundColor Green
}

# Удаляем install.ps1 из скачанного проекта
if (Test-Path "install.ps1") {
    Remove-Item "install.ps1" -Force
    Write-Host "✓ install.ps1 удален" -ForegroundColor Green
}

# Переходим в src
cd src

# Создаем venv
Write-Host "⏳ Создаю виртуальное окружение..." -ForegroundColor Yellow
python -m venv .venv

# Активируем (с обходом политики)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& .\.venv\Scripts\Activate.ps1
Write-Host "✓ Виртуальное окружение активировано" -ForegroundColor Green

# Устанавливаем зависимости
if (Test-Path "requirements.txt") {
    Write-Host "⏳ Устанавливаю зависимости..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "✓ Зависимости установлены" -ForegroundColor Green
}

Write-Host ""
Write-Host "✅ Готово! Запуск:" -ForegroundColor Green
Write-Host "   cd $SERVICE_NAME/src" -ForegroundColor Cyan
Write-Host "   uvicorn app.web_app:app --port 8001" -ForegroundColor Cyan