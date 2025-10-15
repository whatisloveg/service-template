$name = Read-Host "Имя сервиса"
Write-Host "🚀 Клонирую репозиторий..." -ForegroundColor Green
npx degit whatisloveg/service-template $name
cd $name
Write-Host "✓ Репозиторий скопирован" -ForegroundColor Green

Write-Host "⏳ Переименовываю проект в $name..." -ForegroundColor Yellow
if (Test-Path "src/.env.example") {
    Copy-Item src/.env.example src/.env
    (Get-Content src/.env) -replace 'template-service', $name | Set-Content src/.env
}
Write-Host "✓ Проект переименован" -ForegroundColor Green

Write-Host "⏳ Удаляю install скрипты..." -ForegroundColor Yellow
Remove-Item "install.ps1" -Force -ErrorAction SilentlyContinue
Remove-Item "install.sh" -Force -ErrorAction SilentlyContinue
Write-Host "✓ Скрипты удалены" -ForegroundColor Green

Write-Host "⏳ Создаю виртуальное окружение..." -ForegroundColor Yellow
python -m venv .venv
Write-Host "✓ Виртуальное окружение создано" -ForegroundColor Green

Write-Host "⏳ Устанавливаю зависимости..." -ForegroundColor Yellow
& .\.venv\Scripts\pip.exe install -r requirements.txt -q
Write-Host "✓ Зависимости установлены" -ForegroundColor Green

Write-Host ""
Write-Host "✅ Проект $name готов к разработке!" -ForegroundColor Green