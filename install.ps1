$name = Read-Host "Имя сервиса"
Write-Host "🚀 Создаю $name..." -ForegroundColor Green

npx degit whatisloveg/service-template $name
cd $name

if (Test-Path "src/.env.example") {
    Copy-Item src/.env.example src/.env
    (Get-Content src/.env) -replace 'template-service', $name | Set-Content src/.env
}

Remove-Item "install.ps1" -Force -ErrorAction SilentlyContinue

cd src
Write-Host "⏳ Устанавливаю зависимости..." -ForegroundColor Yellow

python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip -q
& .\.venv\Scripts\pip.exe install -r requirements.txt -q

Write-Host "✅ Готово!" -ForegroundColor Green
Write-Host "Запуск:" -ForegroundColor Cyan
Write-Host "  cd $name\src" -ForegroundColor Cyan
Write-Host "  .\.venv\Scripts\activate" -ForegroundColor Cyan
Write-Host "  uvicorn app.web_app:app --port 8001" -ForegroundColor Cyan