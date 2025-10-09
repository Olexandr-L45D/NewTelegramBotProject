# файл по кнопкам keyboards.py
# Тут створюються інлайн-кнопки (меню, варіанти відповідей).
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- Головне меню ---
# додаю кнопку "💤 Сон"
def main_menu_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("💬 Як пройшов день?", callback_data="day"),
        InlineKeyboardButton("📊Інша Статистика", callback_data="stats"),
    )
    kb.add(
        InlineKeyboardButton("⚙️ Налаштування", callback_data="settings"),
        InlineKeyboardButton("Розрахуй BMI", callback_data="bmi"),
    )
    kb.add(
        InlineKeyboardButton("💤 Сон", callback_data="sleep"),
        InlineKeyboardButton("📆 Статистика сну", callback_data="stats_sleep"),
    )
    kb.add(
        InlineKeyboardButton("🔍 Пошук користувачів", callback_data="search"),
        InlineKeyboardButton("👥 Користувачі", callback_data="users"),
    )
    return kb


# --- Кнопки для вибору настрою в менюшці = "💬 Як пройшов день?", callback_data="day"---
def mood_keyboard():
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(
        InlineKeyboardButton("Добре 😊", callback_data="mood_good"),
        InlineKeyboardButton("Так собі 😐", callback_data="mood_ok"),
        InlineKeyboardButton("Погано 😓", callback_data="mood_bad")
    )
    return kb

# --- Клавіатура для вибору кількості годин сну (0.5 год крок) ---
def sleep_keyboard():
    kb = InlineKeyboardMarkup(row_width=3)
    hours_options = [x / 2 for x in range(8, 21)]  # 4.0–10.0
    for h in hours_options:
        kb.insert(InlineKeyboardButton(f"{h} год", callback_data=f"sleep_{h}"))
    kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_menu"))
    return kb

# --- (СТАРИЙ підхід) Клавіатура вибору кількості годин сну --- callback_data="slip"---
# def sleep_keyboard():
#     kb = InlineKeyboardMarkup(row_width=6)
#     kb.add(
#         InlineKeyboardButton("3 год", callback_data="mood_bad"),
#         InlineKeyboardButton("4 год", callback_data="mood_bad"),
#         InlineKeyboardButton("5 год", callback_data="mood_bad"),
#         InlineKeyboardButton("6 год", callback_data="mood_bad"),
#         InlineKeyboardButton("7 год", callback_data="mood_good"),
#         InlineKeyboardButton("8 год", callback_data="mood_good")
#     )
#     return kb

