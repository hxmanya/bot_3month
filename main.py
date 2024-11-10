import asyncio
import logging

from bot_config import bot, dp
from handlers.other_messages import other_messages_router
from handlers.review_dialog import review_router
from handlers.start import start_router
from handlers.bot_commands import commands_router




async def main():
    dp.include_router(start_router)
    dp.include_router(commands_router)
    dp.include_router(review_router)
    dp.include_router(other_messages_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) #loggi
    asyncio.run(main())
