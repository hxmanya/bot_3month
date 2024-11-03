import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import dotenv_values
from random import choice


token = dotenv_values(".env")["BOT_TOKEN"]
bot = Bot(token=token)
dp = Dispatcher()


names = ('Алеша', 'Аман', 'Иван', 'Султан', 'Артём',
         'София', 'Мария', 'Анна', 'Алихан', 'Елена', 'Игорь')

users = set()

@dp.message(Command('start'))
async def start_handler(message: types.Message):
    users.add(message.from_user.id)
    name = message.from_user.first_name
    await message.answer(
        f"Привет, {name}!\n"
        f"Наш бот обслуживает уже {len(users)} пользователей.\n"
        f"Команды бота: \n"
        f"/start - Начать работу\n"
        f"/myinfo - Информация о позьзователе\n"
        f"/random - Случайное имя из списка\n"
    )


@dp.message(Command('myinfo'))
async def myinfo_handler(message: types.Message):
    await message.answer(
        f"Ваш ID: {message.from_user.id}\n"
        f"Имя: {message.from_user.first_name}\n"
        f"Фамилия: {message.from_user.last_name}\n"
        f"Username: @{message.from_user.username or 'отсутствует'}"
    )


@dp.message(Command('random'))
async def send_random_name(message: types.Message):
    random_name = choice(names)
    await message.answer(f"Случайное имя: {random_name}")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
