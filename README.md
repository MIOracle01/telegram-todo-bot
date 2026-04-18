# 🤖 Telegram ToDo Bot

Асинхронный Telegram-бот для управления задачами на **aiogram 3** и **SQLite**.

## Команды
- `/add <текст>` — добавить задачу
- `/list` — показать все задачи
- `/done <номер>` — отметить выполненной
- `/delete <номер>` — удалить задачу

## Запуск
1. Клонируйте репозиторий
2. Создайте виртуальное окружение: `python3 -m venv venv`
3. Активируйте: `source venv/bin/activate`
4. Установите зависимости: `pip install -r requirements.txt`
5. Создайте файл `.env` с переменной `BOT_TOKEN=ваш_токен`
6. Запустите: `python bot.py`

## Важно для РФ
Из-за блокировок Telegram может потребоваться VPN или прокси.

## Технологии
- Python 3.11
- aiogram 3
- aiosqlite
- python-dotenv
