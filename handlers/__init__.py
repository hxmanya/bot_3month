from aiogram import Router, F

from handlers.other_messages import other_messages_router
from handlers.review_dialog import review_router
from handlers.start import start_router
from handlers.bot_commands import commands_router
from handlers.dishes import dishes_router
from handlers.menu import menu_router

private_router = Router()
private_router.include_router(start_router)
private_router.include_router(commands_router)
private_router.include_router(review_router)
private_router.include_router(dishes_router)
private_router.include_router(menu_router)
private_router.include_router(other_messages_router)

private_router.message.filter(F.chat.type == "private")
private_router.callback_query.filter(F.chat.type == "private")


