# db.py
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

import os

# Завантажуємо змінні середовища з .env файлу
load_dotenv()

# Отримуємо URI з .env
MONGO_URI = os.getenv("MONGO_URI")

# Створюємо клієнт
client = MongoClient(MONGO_URI)

# Підключаємо базу telegram_bot
db = client["telegram_bot"]

# (опціонально) створюємо колекцію користувачів
users_collection = db["users"]

# Тест підключення
try:
    client.admin.command("ping")
    print("✅ Підключення до MongoDB успішне!")
except Exception as e:
    print("❌ Помилка підключення:", e)

# --- додати цю функцію add_user ---
async def add_user(user_id: int, username: str):
    """Додає користувача, якщо його ще немає у колекції"""
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({"user_id": user_id, "username": username})

# 🆕 Додаємо функцію для збереження користувача

def add_user_sync(user_id, username, first_name=None, last_name=None):
    """Додає користувача, якщо його ще немає"""
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({
            "user_id": user_id,
            "username": username or "—",
            "first_name": first_name or "",
            "last_name": last_name or "",
        })
# 🔸 Так бот залишиться асинхронним, але роботу з базою віддасть у окремий потік — не блокує події Telegram.
# Це синхронна функція, щоб легко викликати її через asyncio.to_thread() з асинхронних хендлерів.

conversation_collection = db["conversations"]

def log_conversation_sync(user_id, username, text, stage):
    """Зберігає повідомлення користувача або стан діалогу"""
    doc = {
        "user_id": user_id,
        "username": username,
        "text": text,
        "stage": stage,  # наприклад: "day_mood" або "day_detail"
        "timestamp": datetime.utcnow()
    }
    conversation_collection.insert_one(doc)            
