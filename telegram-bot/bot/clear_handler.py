from aiogram import types, Router
from aiogram.filters import Command

router = Router()

@router.message(Command("clear"))
async def clear_chat(message: types.Message):
    """
    🧹 Команда для очищення чату користувача.
    Видаляє останні 50 повідомлень у поточному чаті.
    """
    chat_id = message.chat.id
    user_id = message.from_user.id

    await message.answer("🧹 Очищаю чат...")

    try:
        for i in range(50):  # можна збільшити або зменшити
            msg_id = message.message_id - i
            await message.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        await message.answer("✅ Чат очищено!")
    except Exception as e:
        await message.answer("⚠️ Не всі повідомлення можна видалити (Telegram має обмеження).")
        print(f"Помилка видалення: {e}")
