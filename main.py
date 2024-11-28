import asyncio
import logging

from bot_config import bot, dp, database
from handlers import private_router
from handlers.in_groups import group_router



async def on_startup(bot):
    database.create_tables()


async def main():
    dp.include_router(private_router)
    dp.include_router(group_router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) #loggi
    asyncio.run(main())
