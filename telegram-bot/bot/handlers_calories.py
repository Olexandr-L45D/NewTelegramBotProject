# boot/handlers_calories (окремий MODULE файл суто під функціонал трекеру calories)
from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.keyboards import calories_keyboard, CALORIE_BASE, main_menu_keyboard
from bot.states import CaloriesTracker

# --- Формула Міфліна-Сан Жора ---
def mifflin_st_jeor(weight, height, age, gender="female"):
    s = -161 if gender.lower() == "female" else 5
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + s
    return round(bmr, 1)


# 🆕 Початок трекера калорій
async def calories_start_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🍎 Обери, що ти сьогодні їла/їв — я підрахую орієнтовно з розрахунку на 100г продукту:",
        reply_markup=calories_keyboard()
    )
    await CaloriesTracker.waiting_for_selection.set()
    await state.update_data(selected_food=[])
    await callback.answer()


# 🆕 Обробка вибору/зняття вибору продукту
async def calories_food_select(callback: types.CallbackQuery, state: FSMContext):
    food_name = callback.data.replace("food_", "")
    data = await state.get_data()
    selected = data.get("selected_food", [])

    if food_name in selected:
        selected.remove(food_name)
    else:
        selected.append(food_name)

    await state.update_data(selected_food=selected)
    await callback.message.edit_reply_markup(reply_markup=calories_keyboard(selected))
    await callback.answer()


# 🆕 Підрахунок калорій
async def calories_calculate(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = data.get("selected_food", [])

    if not selected:
        await callback.answer("⚠️ Спочатку обери хоча б один продукт!", show_alert=True)
        return

    total = sum(CALORIE_BASE[f] for f in selected)
    await callback.message.answer(
        f"🍽 Ти обрала/обрав:\n\n" +
        "\n".join([f"• {f} — {CALORIE_BASE[f]} ккал" for f in selected]) +
        f"\n\n🔸 Разом: <b>{total} ккал</b>\n\n"
        "Для довідки: середня добова норма за формулою Міфліна–Сан Жора ~1800–2000 ккал.",
        parse_mode="HTML",
        reply_markup=main_menu_keyboard()
    )

    await state.finish()
    await callback.answer()
