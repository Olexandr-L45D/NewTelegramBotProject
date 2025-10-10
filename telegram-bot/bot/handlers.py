# handlers.py
# Тут логіка реакції на повідомлення/команди користувача (/start, /users, “Привіт!” тощо).

import asyncio
from aiogram import types
from datetime import datetime
from database.db import users_collection, add_user_sync, log_conversation_sync
from bot.keyboards import main_menu_keyboard, mood_keyboard
from bot.states import DayCheck
from aiogram.dispatcher import FSMContext


async def start_handler(message: types.Message):
    # ✅ Додаємо користувача у базу
    await asyncio.to_thread(
        add_user_sync,
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name
    )

    # ✅ Показуємо головне меню
    await message.answer(
        "👋 Привіт! Я твій асистент здоров’я 🧘‍♀️\n\nОбери, що хочеш зробити:",
        reply_markup=main_menu_keyboard()
    )
# Але  тепер бот залишиться асинхронним, але роботу з базою віддасть у окремий потік — не блокує події Telegram.
async def callback_handler(callback: types.CallbackQuery):
    data = callback.data
    chat_id = callback.message.chat.id

    if data == "day":
        await callback.message.answer("Як пройшов твій день? Обери варіант 👇", reply_markup=mood_keyboard())
        await DayCheck.waiting_for_mood.set()

    elif data == "stats":
        await callback.message.answer("📊 Тут буде твоя статистика за останній тиждень!")

    elif data == "search":
        await callback.message.answer("🔍 Введи ім’я користувача для пошуку:")

    elif data == "users":
        users = list(users_collection.find({}))
        if not users:
            await callback.message.answer("😕 У базі ще немає користувачів.")
        else:
            text_lines = ["👥 Збережені користувачі:"]
            for i, user in enumerate(users, 1):
                uname = f"@{user.get('username')}" if user.get("username") else "—"
                full_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip() or "Без імені"
                uid = user.get("user_id", "—")
                text_lines.append(f"{i}. {full_name} ({uname}) — {uid}")
            await callback.message.answer("\n".join(text_lines))

    elif data == "settings":
        await callback.message.answer("⚙️ Меню налаштувань:\n- Змінити мову\n- Отримувати сповіщення про нагадування")

    await callback.answer()

async def save_handler(message: types.Message):
    doc = {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "text": message.text.replace("/save", "").strip() or "Без тексту",
        "created_at": datetime.utcnow()
    }
    users_collection.insert_one(doc)
    await message.reply("✅ Збережено в базі!")

async def id_handler(message: types.Message):
    await message.reply(f"🔹 Твій Telegram ID: {message.from_user.id}")

#  Новий хендлер для /users - отримую список всих користувачів при натсиканні на кнопку

async def users_handler(message: types.Message):
    users = list(users_collection.find({}))
    if not users:
        await message.reply("😕 У базі ще немає користувачів.")
        return

    text_lines = ["👥 Збережені користувачі:"]
    for i, user in enumerate(users, 1):
        uname = f"@{user.get('username')}" if user.get("username") else "—"
        full_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip() or "Без імені"
        uid = user.get("user_id", "—")
        text_lines.append(f"{i}. {full_name} ({uname}) — {uid}")

    text = "\n".join(text_lines)
    await message.reply(text)

# --- новий “дружній” функціонал ---
async def daycheck_start_handler(message: types.Message):
    """Запускає діалог 'Як пройшов твій день?'"""
    await message.answer("Як пройшов твій день? Обери варіант 👇", reply_markup=mood_keyboard())
    await DayCheck.waiting_for_mood.set()

async def mood_handler(callback: types.CallbackQuery, state: FSMContext):
    """Обробляє вибір настрою"""
    mood_map = {
        "mood_good": "Добре 😊",
        "mood_ok": "Так собі 😐",
        "mood_bad": "Погано 😓"
    }
    mood = mood_map.get(callback.data, "Невідомо")
    await asyncio.to_thread(log_conversation_sync, callback.from_user.id, callback.from_user.username, mood, "day_mood")

    await callback.message.answer("Хочеш розповісти детальніше? Напиши кілька слів або введи /skip, щоб пропустити 🙂")
    await DayCheck.waiting_for_detail.set()
    await callback.answer()

async def detail_handler(message: types.Message, state: FSMContext):
    """Обробка тексту, якщо користувач вирішив поділитись деталями"""
    detail = message.text
    await asyncio.to_thread(log_conversation_sync, message.from_user.id, message.from_user.username, detail, "day_detail")
    await message.answer("Дякую, що поділився 💛 Якщо треба — можу надіслати мотивацію або пораду 😉")
    await state.finish()

async def skip_detail_handler(message: types.Message, state: FSMContext):
    """Коли користувач вирішив пропустити деталі"""
    await message.answer("Ок 😊 Якщо захочеш — розповіси пізніше.")
    await state.finish()    

async def back_to_menu_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """Обробник кнопки '⬅️ Назад' — повернення в головне меню."""

    await state.finish() 
    await callback_query.answer()  # обов’язково, щоб Telegram не показував "годинник"    

    await callback_query.message.edit_text(
        "🏠 Ви повернулись у головне меню:",
        reply_markup=main_menu_keyboard()
    )

async def back_to_menu_from_calories(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.finish()
    await callback_query.message.edit_text(
        "🏠 Ви повернулись у головне меню:",
        reply_markup=main_menu_keyboard()
    )

# async def back_to_menu_from_sleep(callback_query: types.CallbackQuery, state: FSMContext):
#     await callback_query.answer()
#     await state.finish()
#     await callback_query.message.edit_text(
#         "🌙 Меню сну:",
#         reply_markup=sleep_menu_keyboard()
#     )

   

#     @dp.callback_query_handler(lambda c: c.data.startswith("back"))
# async def process_any_back(callback_query: types.CallbackQuery, state: FSMContext):
#     await state.finish()
#     await callback_query.message.edit_text(
#         "🔙 Повернувся в головне меню:", 
#         reply_markup=main_menu_keyboard
#     )

