from aiogram import Router, types
from aiogram.filters import Command
from bot_config import users

start_router = Router()


@start_router.message(Command('start'))
async def start_handler(message: types.Message):
    users.add(message.from_user.id)
    name = message.from_user.first_name
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    url="https://www.instagram.com/neymarjr",
                    text="Наш инстаграм"
                ),
                types.InlineKeyboardButton(
                    url="https://online.geeks.kg/",
                    text="Наш сайт"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Оставить отзыв",
                    callback_data="review"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Меню", callback_data="menu"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Добавить блюдо", callback_data="add_dish"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Добавить Категорию", callback_data="add_category"
                )
            ]
        ]
    )
    await message.answer(
        f"Здравствуйте, {name}!\n"
        f"Наш бот обслуживает уже {len(users)} пользователей.\n"
        f"Команды бота: \n"
        f"/start - Начать работу\n"
        f"/myinfo - Информация о позьзователе\n"
        f"/random - Случайный рецепт\n",
        reply_markup=kb
    )