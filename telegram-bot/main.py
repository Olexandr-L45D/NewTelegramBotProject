# main.py — головний файл запуску Telegram-бота
# Підтримує роботу локально й на Railway. Має опціональний keep_alive для web-хостингу.

import os
import asyncio
import aiohttp
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
    raise ValueError("❌ BOT_TOKEN не знайдено! Додай його у Variables Railway або у .env")

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
    back_to_menu_handler,
    back_to_menu_from_calories,
)
from bot.handlers_bmi import start_bmi, process_height, process_weight, process_age
from bot.handlers_sleep import (
    sleep_start_handler,
    sleep_hours_callback_handler,
    sleep_stats_handler
)
from bot.handlers_calories import (
    calories_start_handler,
    calories_food_select,
    calories_calculate
)

from bot.states import DayCheck, BMIForm, CaloriesTracker

# --- Ініціалізація бота ---
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# --- Команди в меню Telegram --- "📊 Підрахувати калорії"
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="🤖 Почати роботу з ботом"),
        BotCommand(command="sleep", description="💤 Трекер сну"),
        BotCommand(command="calories", description="📊 Трекер калорій"),
        BotCommand(command="save", description="💾 Зберегти повідомлення"),
        BotCommand(command="day", description="💬 Як пройшов день?"),
        BotCommand(command="id", description="🆔 Отримати свій Telegram ID"),
        BotCommand(command="users", description="👥 Список користувачів"),
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
# --- Реєстрація нових хендлерів для трекера годин сну---
dp.register_callback_query_handler(sleep_start_handler, lambda c: c.data == "sleep")
dp.register_callback_query_handler(sleep_hours_callback_handler, lambda c: c.data.startswith("sleep_"))
dp.register_callback_query_handler(sleep_stats_handler, lambda c: c.data == "stats_sleep")


dp.register_message_handler(start_handler, Command("start"))
dp.register_message_handler(save_handler, Command("save"))
dp.register_message_handler(id_handler, Command("id"))
dp.register_message_handler(users_handler, Command("users"))
dp.register_message_handler(daycheck_start_handler, Command("day"))

dp.register_callback_query_handler(
    mood_handler,
    lambda c: c.data.startswith("mood"),
    state=DayCheck.waiting_for_mood,
)
dp.register_message_handler(detail_handler, state=DayCheck.waiting_for_detail)
dp.register_message_handler(skip_detail_handler, commands=["skip"], state=DayCheck.waiting_for_detail)

# 🆕 Реєстрація хендлерів для трекера калорій
dp.register_callback_query_handler(calories_start_handler, lambda c: c.data == "calories")
dp.register_callback_query_handler(calories_food_select, lambda c: c.data.startswith("food_"), state=CaloriesTracker.waiting_for_selection)
dp.register_callback_query_handler(calories_calculate, lambda c: c.data == "calc_calories", state=CaloriesTracker.waiting_for_selection)

# 🔙 Обробка кнопки "Назад"
dp.register_callback_query_handler(back_to_menu_handler, lambda c: c.data == "back_to_menu", state="*")

# dp.register_callback_query_handler(back_to_menu_from_sleep, lambda c: c.data == "back_to_menu", state=SleepTracker.waiting_for_hours)
dp.register_callback_query_handler(back_to_menu_from_calories, lambda c: c.data == "back_to_menu", state=CaloriesTracker.waiting_for_selection)



# УВАГА! Загальний обробник в самому кінці !
dp.register_callback_query_handler(callback_handler)

# --- Опціональний асинхронний keep_alive (для Flask/FastAPI версій) ---
async def keep_alive(url: str):
    """Асинхронно пінгує Railway-домен, щоб уникнути сну (для web-деплою)."""
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(url) as resp:
                    print(f"🔁 Keep-alive ping ({resp.status})")
            except Exception as e:
                print(f"⚠️ Keep-alive error: {e}")
            await asyncio.sleep(600)  # кожні 10 хвилин


# --- Запуск Бота ---
if __name__ == "__main__":
    async def on_startup(_):
        await set_commands(bot)
        print("✅ Команди встановлено!")
        print("🤖 Бот запущено та готовий до роботи!")

        # 🔹 Якщо колись додаси Flask/FastAPI і Railway надає домен — розкоментуй нижче:
        # asyncio.create_task(keep_alive('https://mybot.up.railway.app'))

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


