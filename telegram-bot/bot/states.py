# bot/states.py
# Тут описані “стани діалогу” FSM (finite state machine) (проміжни стани між відповідями) — наприклад, “чекаю на оцінку настрою”, “чекаю на деталі дня”.

from aiogram.dispatcher.filters.state import State, StatesGroup

# FSM — набір станів (етапів діалогу)
class DayCheck(StatesGroup):
    waiting_for_mood = State()   # Коли бот чекає, щоб користувач обрав настрій
    waiting_for_detail = State() # Коли бот чекає, щоб користувач описав день детальніше
    confirmation = State()

# додай новий CLASS станів (FSM) для BMI:

class BMIForm(StatesGroup):
    waiting_for_height = State()
    waiting_for_weight = State()
    waiting_for_age = State()


#     user_weight = float(input('Your weight, kg ?'))
# user_height = float(input('Your height, m ?'))
# BMI2 = user_weight/(user_height**2)
# BMI2 = round(BMI2,2)
# print('Your BMI2 equals: ' + str(BMI2))
# if BMI2 <= 18.4:
#     print('You have underweight!')
# elif BMI2 <= 24.9:
#     print('You weight is normal!')
# elif BMI2 <= 39.9:
#     print('You have overweight!')
# else:
#     print('Sorry! You have obese!!!')
