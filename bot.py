import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
import aiosqlite

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def init_db():
    async with aiosqlite.connect("todos.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                task TEXT,
                done BOOLEAN DEFAULT 0
            )
        """)
        await db.commit()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Я ToDo-бот.\n"
                         "/add <текст> — добавить задачу\n"
                         "/list — показать задачи\n"
                         "/done <номер> — отметить задачу выполненной\n"
                         "/delete <номер> — удалить задачу")

@dp.message(Command("add"))
async def add_task(message: Message):
    task_text = message.text.replace("/add", "").strip()
    if not task_text:
        await message.answer("Напишите задачу после команды: /add Купить молоко")
        return
    user_id = message.from_user.id
    async with aiosqlite.connect("todos.db") as db:
        await db.execute("INSERT INTO todos (user_id, task) VALUES (?, ?)", (user_id, task_text))
        await db.commit()
    await message.answer(f"✅ Задача добавлена: {task_text}")

@dp.message(Command("list"))
async def list_tasks(message: Message):
    user_id = message.from_user.id
    async with aiosqlite.connect("todos.db") as db:
        cursor = await db.execute("SELECT id, task, done FROM todos WHERE user_id = ? ORDER BY id", (user_id,))
        rows = await cursor.fetchall()
    if not rows:
        await message.answer("📭 У вас пока нет задач.")
        return
    answer = "📋 Ваши задачи:\n"
    for row in rows:
        status = "✅" if row[2] else "❌"
        answer += f"{row[0]}. {status} {row[1]}\n"
    await message.answer(answer)

@dp.message(Command("done"))
async def done_task(message: Message):
    try:
        task_id = int(message.text.replace("/done", "").strip())
    except ValueError:
        await message.answer("Укажите номер задачи: /done 2")
        return
    user_id = message.from_user.id
    async with aiosqlite.connect("todos.db") as db:
        cursor = await db.execute("SELECT id FROM todos WHERE id = ? AND user_id = ?", (task_id, user_id))
        if not await cursor.fetchone():
            await message.answer("❌ Задача с таким номером не найдена.")
            return
        await db.execute("UPDATE todos SET done = 1 WHERE id = ?", (task_id,))
        await db.commit()
    await message.answer(f"✅ Задача №{task_id} отмечена выполненной!")

@dp.message(Command("delete"))
async def delete_task(message: Message):
    try:
        task_id = int(message.text.replace("/delete", "").strip())
    except ValueError:
        await message.answer("Укажите номер задачи: /delete 2")
        return
    user_id = message.from_user.id
    async with aiosqlite.connect("todos.db") as db:
        cursor = await db.execute("SELECT id FROM todos WHERE id = ? AND user_id = ?", (task_id, user_id))
        if not await cursor.fetchone():
            await message.answer("❌ Задача с таким номером не найдена.")
            return
        await db.execute("DELETE FROM todos WHERE id = ?", (task_id,))
        await db.commit()
    await message.answer(f"🗑 Задача №{task_id} удалена.")

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
