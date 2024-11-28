
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import ChatPermissions
from bot_config import BAD_WORDS
from datetime import datetime, timedelta

group_router = Router()


@group_router.message(Command("ban", prefix="!"))
async def ban_user(message: types.Message):
    if not message.reply_to_message:
        await message.answer("Ответьте на сообщение, которое хотите забанить.")
    else:
        id = message.reply_to_message.from_user.id
        await message.bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=id,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await message.answer(
            f"Пользователь {message.reply_to_message.from_user.full_name} ограничен."
        )


@group_router.message(Command("unban", prefix="!"))
async def unban_user(message: types.Message):
    if not message.reply_to_message:
        await message.answer("Ответьте на сообщение пользователя, чтобы снять ограничения.")
    else:
        id = message.reply_to_message.from_user.id
        await message.bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=id,
            permissions=ChatPermissions(can_send_messages=True)
        )
        await message.answer(f"Пользователь {message.reply_to_message.from_user.full_name} "
                             f"снова активен.")

@group_router.message(F.text.contains("бан"))
async def text_ban_user(message: types.Message):
    if not message.reply_to_message:
        await message.answer("Ответьте на сообщение, которое хотите забанить.")
        return
    parsed_txt = message.text.lower().split()
    print(parsed_txt)
    id = message.reply_to_message.from_user.id
    if len(parsed_txt) == 1:
        await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=id)
        await message.answer(f"Пользователь {message.reply_to_message.from_user.full_name} забанен.")
    elif len(parsed_txt) == 2 and parsed_txt[1] == "1д":
        until_date = datetime.now() + timedelta(days=1)
        await message.bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=id,
            until_date=until_date,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await message.answer(
            f"Пользователь {message.reply_to_message.from_user.full_name} "
            f"забанен на 1д"
        )
    elif len(parsed_txt) == 2 and parsed_txt[1] == "3н":
        until_date = datetime.now() + timedelta(weeks=3)
        await message.bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=id,
            until_date=until_date,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await message.answer(
            f"Пользователь {message.reply_to_message.from_user.full_name} "
            f"забанен на 3н"
        )
    elif len(parsed_txt) == 2 and parsed_txt[1] == "3ч":
        until_date = datetime.now() + timedelta(hours=3)
        await message.bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=id,
            until_date=until_date,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await message.answer(
            f"Пользователь {message.reply_to_message.from_user.full_name} "
            f"забанен на 3ч"
        )
    elif len(parsed_txt) == 2 and parsed_txt[1] == "10м":
        until_date = datetime.now() + timedelta(minutes=10)
        await message.bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=id,
            until_date=until_date,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await message.answer(
            f"Пользователь {message.reply_to_message.from_user.full_name} "
            f"забанен на 10м"
        )
    elif len(parsed_txt) == 2 and parsed_txt[1] == "1м":
        until_date = datetime.now() + timedelta(minutes=1)
        await message.bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=id,
            until_date=until_date,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await message.answer(
            f"Пользователь {message.reply_to_message.from_user.full_name} "
            f"забанен на 1м"
        )
    else:
        await message.answer("Неверный формат времени. Используйте: '1д', '3ч', '3н', '10м', '1м'")



@group_router.message(F.text)
async def check_for_bad_words(message: types.Message):
    message_text = message.text.lower()
    for word in BAD_WORDS:
        if word in message_text:
            user_id = message.from_user.id
            await message.bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
                permissions=ChatPermissions(can_send_messages=False)
            )
            await message.answer(
                f"Пользователь {message.from_user.full_name} ограничен "
                f"за использование запрещённых слов."
            )
            break

