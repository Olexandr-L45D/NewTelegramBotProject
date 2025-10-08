from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.states import BMIForm

# --- Початок BMI-діалогу ---
async def start_bmi(callback: types.CallbackQuery):
    """Запитує зріст користувача"""
    await callback.message.answer("📏 Введи свій зріст у метрах (наприклад, 1.75):")
    await BMIForm.waiting_for_height.set()
    await callback.answer()


# --- Збір зросту ---
async def process_height(message: types.Message, state: FSMContext):
    try:
        height = float(message.text.replace(",", "."))
        if not 0.5 < height < 2.5:
            raise ValueError
        await state.update_data(height=height)
        await message.answer("⚖️ Введи свою вагу в кг (наприклад, 68):")
        await BMIForm.waiting_for_weight.set()
    except ValueError:
        await message.answer("🚫 Введи коректний зріст (від 0.5 до 2.5 м).")


# --- Збір ваги ---
async def process_weight(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text.replace(",", "."))
        if not 20 < weight < 200:
            raise ValueError
        await state.update_data(weight=weight)
        await message.answer("🎂 Введи свій вік:")
        await BMIForm.waiting_for_age.set()
    except ValueError:
        await message.answer("🚫 Введи коректну вагу (від 20 до 200 кг).")


# --- Збір віку та розрахунок BMI ---
async def process_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if not 5 < age < 120:
            raise ValueError

        user_data = await state.get_data()
        height = user_data["height"]
        weight = user_data["weight"]

        bmi = weight / (height ** 2)
        bmi = round(bmi, 2)

        if bmi <= 18.4:
            status = "🔹 У тебе недостатня вага!"
        elif bmi <= 24.9:
            status = "✅ Вага в нормі!"
        elif bmi <= 39.9:
            status = "⚠️ Надмірна вага!"
        else:
            status = "🚨 Ожиріння!"

        await message.answer(
            f"📊 Твій BMI: <b>{bmi}</b>\n{status}",
            parse_mode="HTML"
        )
        await state.finish()

    except ValueError:
        await message.answer("🚫 Введи коректний вік (5–120).")
