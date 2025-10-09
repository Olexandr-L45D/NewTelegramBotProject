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

<!-- Якщо для Хосту- Railway додаю в корінь папки  (Root Directory для Render)-->

├── runtime.txt ← ось СЮДИ додати

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

<!-- ✅ Як запустити long polling бота як Web Service (безкоштовно)
1. У файлі Procfile

Замість

worker: python main.py


пиши:

web: python main.py -->
<!-- old example -->
<!-- aiogram==2.25.1
pymongo==4.3.3
python-dotenv==1.0.1
 -->
<!-- 🔍 Підсумок: встановлені головні бібліотеки

requests ✅ — тепер є

aiogram ✅ — головна бібліотека бота

python-dotenv ✅ — читає .env

pymongo ✅ — для MongoDB

aiohttp, magic-filter ✅ — частини aiogram -->

<!-- Якщо деплою на РЕНДЕР то в файлі  Procfile вказую
web: python main.py-->

<!-- Якщо деплою на Railway то вказую : worker: python main.py
 Це фоновий процес, він не слухає веб-порт, просто виконує main.py.

Railway сприймає worker: як окремий тип сервісу.-->
<!-- Тому для Railway в файлі - ✅ Procfile

Railway має знати, як саме запускати процес:

worker: python main.py
⚠️ Важливо: слово worker (а не web), бо Telegram-бот не обробляє HTTP-запити, а працює як фоновий процес. -->

<!-- Якщо для деплою на Railway потрібні такі налаштування пакетів для бібліотек в файлі
├── requirements.txt:
🔍 Аналіз по рядках
Пакет	Версія	Підтримка Python 3.11	Коментар
aiogram 2.25.1	✅ Так	Стабільно працює на 3.11 (тільки Python 3.12 може видавати warning)
pymongo 4.3.3	✅ Так	Підтримує 3.11; якщо колись буде проблема — можна оновити до 4.8+
python-dotenv 1.0.1	✅ Так	Без проблем
aiohttp 3.8.6	⚠️ Так, але з застереженням	Ця версія офіційно підтримує Python 3.11, але не 3.12+ (і точно не 3.13). Отже, runtime.txt з Python 3.11 → обов’язковий
requests 2.32.3	✅ Так	Повна сумісність
 -->
 <!-- Тому додаю новий файл - 
 ✅ runtime.txt в якому пишу одну єдину залежність =
python-3.11.9
(щоб уникнути проблем із aiohttp і новими версіями Python) -->

<!-- Тому на ХОСТІ Railway
🕒 4. Цілодобова робота

Railway тримає worker-процеси активними постійно, поки:

Проєкт не перевищує ліміти безкоштовного тарифу (якщо ти на free-плані).

main.py працює без винятків.

👉 Щоб не зупинявся:

Не використовуй time.sleep() без асинхронних await-пауc.

Уникай помилок, які можуть завершити цикл.

Можеш додати простий лог:

print("Bot started and running 24/7...") -->

<!-- ЩОБ БОТ не засипав Як вірно зробити ?
✅ Як правильно

Використай асинхронну паузу:
import asyncio
import aiohttp

async def keep_alive(url: str):
    """Асинхронний keep-alive для Railway."""
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(url) as resp:
                    print(f"🔁 Keep-alive ping ({resp.status})")
            except Exception as e:
                print(f"⚠️ Keep-alive error: {e}")
            await asyncio.sleep(600)  # кожні 10 хвилин
 -->

 <!-- І запусти цей цикл паралельно з ботом: -->
 <!-- import asyncio
from aiogram import executor

async def on_startup(dp):
    asyncio.create_task(keep_alive("https://mybot.up.railway.app  ЯКЩО беру згенерований УРЛ проекта на Railway"))
    print("✅ Бот запущено та keep-alive активовано!")

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
 -->
 <!-- ЩОБ не перелімітити на безкоштовному палні такі поради:
 ⚠️ Що це означає для твого Telegram-бота

Бот, який просто спілкується з Telegram API і реагує на повідомлення — навряд “перелімититься” через запити всередині самого бота (бо це небагато запитів: отримати оновлення, відправити повідомлення).

Але якщо ти викликаєш інші API (зовнішні сервіси) багато разів, це додасть навантаження.

Важливі обмеження — RAM/CPU: якщо твій бот раптом почне використовувати багато пам’яті або процесора, він може бути перезапущений або зупинений.

✅ Як зменшити споживання ресурсів і уникнути проблем

Ось деякі прийоми:

Уникай частих опитувань (polling) без потреби
— aiogram polling — це стандарт. Але не додавай додаткові цикли з частими запитами, якщо не треба.

Кешуй дані
Якщо бот звертається до зовнішнього API багато разів за короткий час, збережи результат на деякий час (наприклад, 1–5 хвилин).

Обмежуй довгі або ресурсоємні задачі
Наприклад, не запускай важкі обчислення або великі запити прямо в обробнику повідомлення. Краще винеси у фоновий процес або queue.

Відключай зайві “heartbeat” / ping-и, якщо не потрібно
Як ми вже обговорювали — keep_alive не потрібен у worker-режимі.

Слідкуй за лімітами ресурсів
У Railway — встанови hard usage limit, щоб не було несподіваних витрат 
Railway Docs
.

Моніторинг логів
Періодично дивися в Dashboard → Logs → Deployment logs, щоб бачити, чи бот працює стабільно, чи є помилки через брак пам’яті чи процесора.

Мінімізуй залежності
У requirements.txt — тільки потрібні пакети, без зайвих “важких” бібліотек. -->
