from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from bot.keyboards import main_menu_keyboard

async def clear_chat_handler(callback: types.CallbackQuery, state: FSMContext):
    # Очистка чату (видаляємо останні 50 повідомлень)
    chat_id = callback.message.chat.id
    messages = await callback.message.chat.get_history(limit=50)
    for msg in messages:
        try:
            await callback.message.bot.delete_message(chat_id, msg.message_id)
        except:
            pass
    await callback.message.answer("🧹 Чат очищено!", reply_markup=main_menu_keyboard())
    await callback.answer()

def register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(clear_chat_handler, lambda c: c.data == "clear")
