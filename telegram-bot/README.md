# Telegram Health Bot 💬

Бот для щоденного трекінгу настрою та збереження користувачів у MongoDB.

## 🚀 Функціонал

- /start — стартове вітання
- /users — список користувачів
- /save — збереження повідомлення
- /day — коротке опитування "Як пройшов день?"

## 🧠 Технології

- Python 3.11+
- aiogram 2.x
- MongoDB
- python-dotenv

## ▶️ Запуск

1. Створити `.env` з `BOT_TOKEN` і `MONGO_URI`
2. Активувати середовище:
   ```bash
   .\.venv\Scripts\activate
   ```

NewTelegramBotProject/
│
└── telegram_bot/ ← корінь (Root Directory для Render)
│
├─ bot/ # Основна логіка бота
│ ├─ handlers.py # Обробка командgit
│ ├─ keyboards.py # Інлайн кнопки
│ └─ states.py # FSM (стани діалогів, якщо потрібно)
│
├─ database/ # Модулі для роботи з MongoDB
│ └─ db.py
│
├─ config.py # Токени та налаштування
├─ main.py # Точка входу (запуск бота)
├── requirements.txt ✅ ← цей файл має бути саме тут!
└── .env ⚠️ ← локально можна тримати, але не пушити в Git!

<!-- from aiogram.dispatcher.filters import Command -->

<!-- основні налаштування двигуна  -->
<!-- aiogram==3.0.0b7
motor==3.1.1        # асинхронний драйвер MongoDB
python-dotenv==1.0.0
 -->
<!-- Example .env -->
<!-- BOT_TOKEN=123456789:AAEabcdefGHIjklMNOpqrSTuVwxyz
MONGO_URI=mongodb+srv://user:pass@cluster0.mongodb.net/telegram_bot?retryWrites=true&w=majority
ADMIN_ID=123456789
 -->

 <!-- 🧩 3. Як тепер працює логіка “під капотом”

Користувач вводить /day → daycheck_start_handler

FSM переходить у стан waiting_for_mood

Користувач обирає “Добре 😊” → mood_handler

FSM переходить у стан waiting_for_detail

Користувач або:

пише текст → detail_handler

або вводить /skip → skip_detail_handler

Усі відповіді логуються у MongoDB (колекція conversations)

FSM state.finish() очищає стан користувача -->

<!-- 4. Як розширювати цю логіку

Коли захочеш додати новий тип діалогу (наприклад, “ранкова мотивація” або “опитування про здоров’я”):

Створюєш новий клас у states.py

Додаєш нові хендлери у handlers.py

(за потреби) створюєш нові кнопки у keyboards.py

Реєструєш їх у main.py -->
