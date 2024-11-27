from aiogram import F, Router
from aiogram.types import CallbackQuery
from bot_config import database


menu_router = Router()

@menu_router.callback_query(F.data == "menu")
async def view_all_dishes(callback: CallbackQuery):
    all_dish = database.fetch(query="SELECT name, price, category FROM dishes ORDER BY price ASC")
    response = "Список блюд: \n\n"
    for dish in all_dish:
        response += (
            f"Название: {dish['name']}\n"
            f"Цена: {dish['price']}\n"
            f"Категория: {dish['category']}\n\n"
        )
    await callback.message.answer(response)