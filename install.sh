#!/bin/bash
read -p "Имя сервиса: " name < /dev/tty
echo "🚀 Клонирую репозиторий..."
git clone https://github.com/whatisloveg/service-template "$name"
cd "$name" && rm -rf .git
echo "✓ Репозиторий скопирован"
[ -f src/.env.example ] && cp src/.env.example src/.env && sed -i '' "s/template-service/$name/g" src/.env
echo "✓ Проект переименован"
rm -f install.ps1 install.sh
echo "✓ Скрипты удалены"
python3 -m venv .venv
echo "✓ .venv создан"
.venv/bin/pip install -r requirements.txt -q
echo "✓ Зависимости установлены"
echo ""
echo "✅ Проект $name готов!"