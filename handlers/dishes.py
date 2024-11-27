from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from bot_config import database


dishes_router = Router()
ADMIN_ID = 527117097

class Dish(StatesGroup):
    name = State()
    price = State()
    category = State()

@dishes_router.callback_query(F.data == "add_dish")
async def start_add_dishes(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("У вас нет прав для добавления блюд.", show_alert=True)
        return
    await state.set_state(Dish.name)
    await callback.message.answer("Введите название блюда: ")

@dishes_router.message(Dish.name)
async def process_name(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У вас нет прав для выполнения этого действия.")
        return
    await state.update_data(name=message.text)
    await state.set_state(Dish.price)
    await message.answer("Введите цену блюда: ")

@dishes_router.message(Dish.price)
async def process_price(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У вас нет прав для выполнения этого действия.")
        return
    await state.update_data(price=message.text)
    await state.set_state(Dish.category)
    await message.answer("Введите категорию блюда: ")

@dishes_router.message(Dish.category)
async def process_category(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У вас нет прав для выполнения этого действия.")
        return
    await state.update_data(category=message.text)
    data = await state.get_data()
    database.execute(
        query="""
            INSERT INTO dishes(name, price, category)
            VALUES (?, ?, ?)
        """,
        params=(data["name"], data["price"], data["category"]),
    )
    await message.answer("Блюдо добавлено!")
    await state.clear()