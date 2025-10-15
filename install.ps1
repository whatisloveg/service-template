$SERVICE_NAME = Read-Host "Enter service name"

Write-Host "🚀 Creating $SERVICE_NAME..." -ForegroundColor Green

npx degit whatisloveg/service-template $SERVICE_NAME
cd $SERVICE_NAME/src

Copy-Item .env.example .env
(Get-Content .env) -replace 'template-service', $SERVICE_NAME | Set-Content .env

python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Write-Host "✅ Done! Run: uvicorn app.web_app:app --port 8001" -ForegroundColor Green