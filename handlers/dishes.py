from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from bot_config import database


dishes_router = Router()

dishes_router.message.filter(
    F.from_user.id == 1069749988
    )
dishes_router.callback_query.filter(
    F.from_user.id == 1069749988
    )


class Dish(StatesGroup):
    name = State()
    price = State()
    category = State()

class Category(StatesGroup):
    name = State()

@dishes_router.callback_query(F.data == "add_category")
async def add_category(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Category.name)
    await callback.message.answer("Введи название категории: ")

@dishes_router.message(Category.name)
async def process_category_name(message: types.Message, state: FSMContext):
    new_cat = message.text
    database.execute(
        query="""
            INSERT INTO dish_categories(name)
            VALUES (?)
        """,
        params=(new_cat,)
    )
    await message.answer("Успешно добавлено")
    await state.clear()

@dishes_router.callback_query(F.data == "add_dish")
async def start_add_dishes(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Dish.name)
    await callback.message.answer("Введите название блюда: ")

@dishes_router.message(Dish.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Dish.price)
    await message.answer("Введите цену блюда: ")

@dishes_router.message(Dish.price)
async def process_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(Dish.category)
    # await message.answer("Введите категорию блюда: ")
    categories = database.fetch(query="SELECT name FROM dish_categories")
    if not categories:
        await message.answer(
            "Категорий нет. Добавьте категорию для продолжения"
        )
        await state.clear()
        return
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=cat["name"])] for cat in categories],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    await message.answer("Выберите категорию блюда:", reply_markup=keyboard)


@dishes_router.message(Dish.category)
async def process_category(message: types.Message, state: FSMContext):
    # await state.update_data(category=message.text)
    category = database.fetch(
        query="SELECT id FROM dish_categories WHERE name = ?", params=(message.text,)
    )
    if not category:
        await message.answer("Указанная категория не найдена. Попробуйте снова.")
        return
    category_id = category[0]["id"]
    await state.update_data(category_id=category_id)

    data = await state.get_data()
    database.execute(
        query="""
            INSERT INTO dishes(name, price, category_id)
            VALUES (?, ?, ?)
        """,
        params=(data["name"], data["price"], category_id),
    )
    await message.answer("Блюдо добавлено в меню!", reply_markup=ReplyKeyboardRemove())
    await state.clear()