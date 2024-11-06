from aiogram import Router, types


other_messages_router = Router()

@other_messages_router.message()
async def echo_handler(message: types.Message):
    # обработчик всех сообщений
    await message.answer(message.text)
