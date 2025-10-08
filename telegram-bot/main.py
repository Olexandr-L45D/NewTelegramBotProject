# main.py — головний файл запуску Telegram-бота
# Тут створюється бот, Dispatcher і реєструються всі хендлери.

import os
import time
import threading
import requests
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

# --- Завантаження змінних середовища (.env або Railway Variables) ---
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не знайдено! Додай його у змінні середовища Railway або у .env")

# --- Імпорт хендлерів ---
from bot.handlers import (
    start_handler,
    callback_handler,
    save_handler,
    id_handler,
    users_handler,
    daycheck_start_handler,
    mood_handler,
    detail_handler,
    skip_detail_handler,
)
from bot.handlers_bmi import start_bmi, process_height, process_weight, process_age
from bot.states import DayCheck, BMIForm

# --- Ініціалізація бота ---
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# --- Команди в меню Telegram ---
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="🤖 Почати роботу з ботом"),
        BotCommand(command="save", description="💾 Зберегти повідомлення"),
        BotCommand(command="day", description="💬 Як пройшов день?"),
        BotCommand(command="id", description="🆔 Отримати свій Telegram ID"),
        BotCommand(command="users", description="👥 Список користувачів у базі"),
        BotCommand(command="bmi", description="⚖️ Розрахувати BMI"),
    ]
    await bot.set_my_commands(commands)

# --- Реєстрація callback та FSM хендлерів ---
dp.register_callback_query_handler(start_bmi, lambda c: c.data == "bmi")
dp.register_message_handler(process_height, state=BMIForm.waiting_for_height)
dp.register_message_handler(process_weight, state=BMIForm.waiting_for_weight)
dp.register_message_handler(process_age, state=BMIForm.waiting_for_age)

dp.register_message_handler(daycheck_start_handler, lambda m: m.text == "💬 Як пройшов день?")
dp.register_message_handler(users_handler, lambda m: m.text == "👥 Користувачі")
dp.register_message_handler(id_handler, lambda m: m.text == "🆔 Мій ID")

dp.register_message_handler(start_handler, Command("start"))
dp.register_message_handler(save_handler, Command("save"))
dp.register_message_handler(id_handler, Command("id"))
dp.register_message_handler(users_handler, Command("users"))
dp.register_message_handler(daycheck_start_handler, Command("day"))

dp.register_callback_query_handler(callback_handler)

dp.register_callback_query_handler(
    mood_handler,
    lambda c: c.data.startswith("mood"),
    state=DayCheck.waiting_for_mood,
)
dp.register_message_handler(detail_handler, state=DayCheck.waiting_for_detail)
dp.register_message_handler(skip_detail_handler, commands=["skip"], state=DayCheck.waiting_for_detail)

# --- Keep-alive для Railway (опціонально, щоб не засинав) ---
def keep_alive(url: str):
    """Пінгує твій Railway-домен для запобігання сну (опціонально)."""
    while True:
        try:
            requests.get(url)
            print("🔁 Pinged Railway keep-alive URL.")
        except Exception as e:
            print(f"⚠️ Keep-alive error: {e}")
        time.sleep(600)  # кожні 10 хвилин

# --- Запуск ---
if __name__ == "__main__":
    # Якщо Railway видає власний URL (типу https://mybot.up.railway.app) — можна активувати keep_alive:
    # threading.Thread(target=keep_alive, args=("https://mybot.up.railway.app",), daemon=True).start()

    async def on_startup(_):
        await set_commands(bot)
        print("✅ Команди встановлено!")
        print("🤖 Бот запущено та готовий до роботи!")

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


# # main.py - головний файл запуску - Точка входу (запуск бота) — тут створюється бот, Dispatcher, і реєструються всі хендлери.

# from aiogram import Bot, Dispatcher, executor
# from aiogram.dispatcher.filters import Command
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.types import BotCommand
# import threading
# import requests
# import time

# from bot.handlers import (
#     start_handler,
#     callback_handler,
#     save_handler,
#     id_handler,
#     users_handler,
#     daycheck_start_handler,
#     mood_handler,
#     detail_handler,
#     skip_detail_handler,
# )
# from bot.states import DayCheck
# from config import BOT_TOKEN
# from bot.handlers_bmi import start_bmi, process_height, process_weight, process_age
# from bot.states import BMIForm

# # --- Ініціалізація ---
# bot = Bot(token=BOT_TOKEN)
# storage = MemoryStorage()  # FSM зберігає стани користувачів у пам'яті
# dp = Dispatcher(bot, storage=storage)


# # --- Команди в меню Telegram ---
# async def set_commands(bot: Bot):
#     commands = [
#         BotCommand(command="start", description="🤖 Почати роботу з ботом"),
#         BotCommand(command="save", description="💾 Зберегти повідомлення"),
#         BotCommand(command="day", description="💬 Як пройшов день?"),
#         BotCommand(command="id", description="🆔 Отримати свій Telegram ID"),
#         BotCommand(command="users", description="👥 Список користувачів у базі"),
#         BotCommand(command="bmi", description="🤖 BMI"),
#     ]
#     await bot.set_my_commands(commands)

# # --- Callback кнопки ---
# dp.register_callback_query_handler(start_bmi, lambda c: c.data == "bmi")

# # --- FSM для BMI ---
# dp.register_message_handler(process_height, state=BMIForm.waiting_for_height)
# dp.register_message_handler(process_weight, state=BMIForm.waiting_for_weight)
# dp.register_message_handler(process_age, state=BMIForm.waiting_for_age)

# # --- Хендлери з кнопками (текстові натискання) ---
# dp.register_message_handler(daycheck_start_handler, lambda m: m.text == "💬 Як пройшов день?")
# dp.register_message_handler(users_handler, lambda m: m.text == "👥 Користувачі")
# dp.register_message_handler(id_handler, lambda m: m.text == "🆔 Мій ID")

# # --- Хендлери для стандартних команд ---
# dp.register_message_handler(start_handler, Command("start"))
# dp.register_message_handler(save_handler, Command("save"))
# dp.register_message_handler(id_handler, Command("id"))
# dp.register_message_handler(users_handler, Command("users"))
# dp.register_message_handler(daycheck_start_handler, Command("day"))

# # --- Callback (інлайн кнопки) ---
# dp.register_callback_query_handler(callback_handler)

# # --- FSM логіка (етапи діалогу "Як пройшов день?") ---
# dp.register_callback_query_handler(
#     mood_handler,
#     lambda c: c.data.startswith("mood"),
#     state=DayCheck.waiting_for_mood,
# )
# dp.register_message_handler(detail_handler, state=DayCheck.waiting_for_detail)
# dp.register_message_handler(skip_detail_handler, commands=["skip"], state=DayCheck.waiting_for_detail)

# # --- added new function re-start on Render.com ---
# def keep_alive():
#     url = "https://newtelegrambotproject.onrender.com"
#     while True:
#         try:
#             requests.get(url)
#             print("Pinged Render to stay awake.")
#         except Exception as e:
#             print(f"Keep-alive error: {e}")
#         time.sleep(600)  # кожні 10 хвилин


# # --- Запуск ---
# if __name__ == "__main__":
#     import asyncio
#     import threading

#     threading.Thread(target=keep_alive, daemon=True).start()  # ✅ запуск потоку всередині main

#     async def on_startup(_):
#         await set_commands(bot)
#         print("✅ Команди встановлено!")
#         print("✅ Підключення до MongoDB успішне!")
#         print("🤖 Бот запущено...")

#     executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

# Залишок старого кода без рестарта на РЕНДЕР
# # --- Запуск ---
# if __name__ == "__main__":
#     import asyncio

#     async def on_startup(_):
#         await set_commands(bot)
#         print("✅ Команди встановлено!")
#         print("✅ Підключення до MongoDB успішне!")
#         print("🤖 Бот запущено...")

#     executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

