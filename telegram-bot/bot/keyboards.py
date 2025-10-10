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
     # 🆕 Додаємо кнопку для переходу до калькулятора калорій
    kb.add(InlineKeyboardButton("🍎 Калькулятор калорій", callback_data="calories"))
    
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

# --- 🆕---НОВА Клавіатура для підрахунку кількості калорій  ---
# все приблизно за 100г продукта
CALORIE_BASE = {
    "🍎 Яблуко ": 52,
    "🍌 Банан ": 89,
    "🍓 Полуниця ": 32,
    "🍇 Виноград ": 69,
    "🍍 Ананас ": 50,
    "🍞 Хліб ~30г": 80,  
    "🥚 Яйце (1 шт)": 70,
    "🥚 Яйце ": 155,
    "🥣 Каша вівсяна ": 88,
    "🥣 Каша рис ": 88,
    "🥣 Каша гречка ": 88,
    "🥔 Картопля варена ": 82,
    "🥔 Картопля смажена ": 192,
    "🍚 Рис варений": 130,
    "🍝 Макарони ": 130,
    "🍳 Омлет ": 180,
    "🍗 Курка ": 165,
    "🐟 Риба ": 120,  
    "🥩 Яловичина ": 250,
    "🍖 Свинина ": 290,
    "🥛 Молоко ": 120,
    "🥛 Молоко ": 60,
    "🍶 Йогурт ": 140,
    "🍶 Йогурт ": 70,
    "🥗 Суп овоч ": 90,
    "🥦 Броколі ": 34,
    "🥕 Морква ": 41,
    "🍅 Помідор ": 18,
    "🧀 Сир твердий ": 350,
    "🍫 Шоколад ": 550,
    "🌰 Горіхи волоські ": 650,
    "🌽 Кукурудза свіжа ": 97,
    "☕ Кава з цукром": 30,
}


def calories_keyboard(selected=None):
    """
    Створює клавіатуру для підрахунку калорій.
    selected — список вибраних продуктів (підсвічуються ✅)
    """
    if selected is None:
        selected = []

    kb = InlineKeyboardMarkup(row_width=2)
    for name, kcal in CALORIE_BASE.items():
        label = f"{'✅ ' if name in selected else ''}{name} — {kcal} ккал"
        kb.insert(InlineKeyboardButton(label, callback_data=f"food_{name}"))

    kb.add(
        InlineKeyboardButton("📊 Підрахувати калорії", callback_data="calc_calories"),
    
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_menu")
    )
    return kb



