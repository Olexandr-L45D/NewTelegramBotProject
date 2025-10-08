# main.py - головний файл запуску - Точка входу (запуск бота) — тут створюється бот, Dispatcher, і реєструються всі хендлери.

from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

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
from bot.states import DayCheck
from config import BOT_TOKEN
from bot.handlers_bmi import start_bmi, process_height, process_weight, process_age
from bot.states import BMIForm

# --- Ініціалізація ---
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()  # FSM зберігає стани користувачів у пам'яті
dp = Dispatcher(bot, storage=storage)


# --- Команди в меню Telegram ---
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="🤖 Почати роботу з ботом"),
        BotCommand(command="save", description="💾 Зберегти повідомлення"),
        BotCommand(command="day", description="💬 Як пройшов день?"),
        BotCommand(command="id", description="🆔 Отримати свій Telegram ID"),
        BotCommand(command="users", description="👥 Список користувачів у базі"),
        BotCommand(command="bmi", description="🤖 BMI"),
    ]
    await bot.set_my_commands(commands)

# --- Callback кнопки ---
dp.register_callback_query_handler(start_bmi, lambda c: c.data == "bmi")

# --- FSM для BMI ---
dp.register_message_handler(process_height, state=BMIForm.waiting_for_height)
dp.register_message_handler(process_weight, state=BMIForm.waiting_for_weight)
dp.register_message_handler(process_age, state=BMIForm.waiting_for_age)

# --- Хендлери з кнопками (текстові натискання) ---
dp.register_message_handler(daycheck_start_handler, lambda m: m.text == "💬 Як пройшов день?")
dp.register_message_handler(users_handler, lambda m: m.text == "👥 Користувачі")
dp.register_message_handler(id_handler, lambda m: m.text == "🆔 Мій ID")

# --- Хендлери для стандартних команд ---
dp.register_message_handler(start_handler, Command("start"))
dp.register_message_handler(save_handler, Command("save"))
dp.register_message_handler(id_handler, Command("id"))
dp.register_message_handler(users_handler, Command("users"))
dp.register_message_handler(daycheck_start_handler, Command("day"))

# --- Callback (інлайн кнопки) ---
dp.register_callback_query_handler(callback_handler)

# --- FSM логіка (етапи діалогу "Як пройшов день?") ---
dp.register_callback_query_handler(
    mood_handler,
    lambda c: c.data.startswith("mood"),
    state=DayCheck.waiting_for_mood,
)
dp.register_message_handler(detail_handler, state=DayCheck.waiting_for_detail)
dp.register_message_handler(skip_detail_handler, commands=["skip"], state=DayCheck.waiting_for_detail)


# --- Запуск ---
if __name__ == "__main__":
    import asyncio

    async def on_startup(_):
        await set_commands(bot)
        print("✅ Команди встановлено!")
        print("✅ Підключення до MongoDB успішне!")
        print("🤖 Бот запущено...")

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

