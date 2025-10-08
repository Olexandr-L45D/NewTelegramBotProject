# файл по кнопкам keyboards.py
# Тут створюються інлайн-кнопки (меню, варіанти відповідей).
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- Головне меню ---
# додаю кнопку BMI
def main_menu_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("💬 Як пройшов день?", callback_data="day"),
        InlineKeyboardButton("📊 Статистика", callback_data="stats"),
    )
    kb.add(
        InlineKeyboardButton("🔍 Пошук користувачів", callback_data="search"),
        InlineKeyboardButton("👥 Користувачі", callback_data="users"),
    )
    kb.add(
        InlineKeyboardButton("⚙️ Налаштування", callback_data="settings"),
        InlineKeyboardButton("Розрахуй BMI", callback_data="bmi"),
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
