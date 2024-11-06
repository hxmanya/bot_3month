from aiogram import Router, types
from aiogram.filters import Command
from random import choice

from aiogram.types import FSInputFile
from bot_config import recipes

commands_router = Router()

@commands_router.message(Command('myinfo'))
async def myinfo_handler(message: types.Message):
    await message.answer(
        f"Ваш ID: {message.from_user.id}\n"
        f"Имя: {message.from_user.first_name}\n"
        f"Фамилия: {message.from_user.last_name}\n"
        f"Username: @{message.from_user.username or 'отсутствует'}"
    )


@commands_router.message(Command('random'))
async def send_random_name(message: types.Message):
    random_recipe = choice(recipes)
    caption = (f"{random_recipe['name']}:\n"
               f"{random_recipe['recipe']}")
    photo = FSInputFile(random_recipe['photo_path'])
    await message.answer_photo(photo=photo, caption=caption)


