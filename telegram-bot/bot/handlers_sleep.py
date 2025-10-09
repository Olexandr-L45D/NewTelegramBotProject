# boot/handlers_sleep (окремий файл суто під функціонал трекеру годин сну)
from aiogram import types
from datetime import datetime, timedelta
from bot.keyboards import main_menu_keyboard, sleep_keyboard
from database.db import sleep_collection

# 💤 Початок трекера сну
async def sleep_start_handler(callback: types.CallbackQuery):
    await callback.message.answer(
        "🌙 Скільки годин ти сьогодні спала?", reply_markup=sleep_keyboard()
    )
    await callback.answer()


# 💤 Обробка вибору годин (callback)
async def sleep_hours_callback_handler(callback: types.CallbackQuery):
    data = callback.data
    if data == "back_to_menu":
        await callback.message.answer("Повертаюсь у головне меню:", reply_markup=main_menu_keyboard())
        await callback.answer()
        return

    # Отримуємо годинник з callback_data (sleep_6.5 → 6.5)
    hours = float(data.replace("sleep_", ""))
    user_id = callback.from_user.id
    today = datetime.now().strftime("%Y-%m-%d")

    # --- Зберігаємо у MongoDB ---
    sleep_collection.update_one(
        {"user_id": user_id, "date": today},
        {"$set": {"hours": hours}},
        upsert=True
    )

    # --- Розрахунок середнього за 7 днів ---
    seven_days_ago = datetime.now() - timedelta(days=7)
    last_week_data = list(sleep_collection.find({
        "user_id": user_id,
        "date": {"$gte": seven_days_ago.strftime("%Y-%m-%d")}
    }).sort("date", -1))

    avg_sleep = round(sum(i["hours"] for i in last_week_data) / len(last_week_data), 1) if last_week_data else hours

    # --- Перевірка 3 днів поспіль < 7 год ---
    recent_days = list(sleep_collection.find({"user_id": user_id}).sort("date", -1).limit(3))
    low_sleep_days = [i for i in recent_days if i["hours"] < 7.0]

    if len(low_sleep_days) >= 3:
        warning = "\n⚠️ Ти спала менше 7 годин кілька днів поспіль.\nСпробуй раніше лягати 💖"
    elif hours < 6.0:
        warning = "\n😴 Твій сон був занадто короткий! Відпочинь більше 💫"
    else:
        warning = ""

    await callback.message.answer(
        f"✅ Збережено {hours:.1f} год сну!\n"
        f"📊 Середній сон за тиждень: {avg_sleep:.1f} годин{warning}",
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()


# 📆 Статистика сну
async def sleep_stats_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    last_week_data = list(
        sleep_collection.find({"user_id": user_id}).sort("date", -1).limit(7)
    )

    if not last_week_data:
        await callback.message.answer("Немає даних про сон 😴", reply_markup=main_menu_keyboard())
        await callback.answer()
        return

    # Формуємо таблицю
    rows = [
        f"{d['date']} — {d['hours']} год"
        for d in sorted(last_week_data, key=lambda x: x["date"], reverse=True)
    ]
    avg_sleep = round(sum(i["hours"] for i in last_week_data) / len(last_week_data), 1)
    text = "📆 *Твоя статистика сну за останні 7 днів:*\n\n" + "\n".join(rows)
    text += f"\n\n📊 *Середній сон:* {avg_sleep:.1f} год"

    await callback.message.answer(text, parse_mode="Markdown", reply_markup=main_menu_keyboard())
    await callback.answer()
