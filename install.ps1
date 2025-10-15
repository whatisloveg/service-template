$SERVICE_NAME = Read-Host "Введите имя сервиса"
$TARGET_DIR = Join-Path (Get-Location) $SERVICE_NAME

Write-Host "🚀 Создаю $SERVICE_NAME..." -ForegroundColor Green

npx degit whatisloveg/service-template $TARGET_DIR

if (-not (Test-Path $TARGET_DIR)) {
    Write-Host "❌ Ошибка создания проекта" -ForegroundColor Red
    exit 1
}

cd $TARGET_DIR

# Проверяем и копируем .env
if (Test-Path "src/.env.example") {
    Copy-Item src/.env.example src/.env
    (Get-Content src/.env) -replace 'template-service', $SERVICE_NAME | Set-Content src/.env
    Write-Host "✓ .env настроен" -ForegroundColor Green
}

# Удаляем install.ps1
if (Test-Path "install.ps1") {
    Remove-Item "install.ps1" -Force
}

cd src

Write-Host "⏳ Создаю виртуальное окружение..." -ForegroundColor Yellow
python -m venv .venv

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
& .\.venv\Scripts\Activate.ps1

Write-Host "⏳ Устанавливаю зависимости..." -ForegroundColor Yellow
pip install -r requirements.txt -q

Write-Host ""
Write-Host "✅ Готово! Запуск:" -ForegroundColor Green
Write-Host "   cd $SERVICE_NAME\src" -ForegroundColor Cyan
Write-Host "   uvicorn app.web_app:app --port 8001" -ForegroundColor Cyan