from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.services.database import get_or_create_user, get_or_create_group, database_save_message, get_recent_messages
from bot.services.llm import generate_reply

router = Router()

@router.message(Command("ghost"))
async def ghost_command(message: Message):
    user_name = message.from_user.first_name
    telegram_id = message.from_user.id
    tele_handle = message.from_user.username

    telegram_chat_id = message.chat.id
    chat_name = message.chat.title

    # Get user and group from DB
    user = get_or_create_user(telegram_id, tele_handle, user_name)
    group = get_or_create_group(telegram_chat_id, chat_name)

    if not user or not group:
        await message.answer("Error: Could not access database")
        return

    # Get recent messages and generate reply
    recent_messages = get_recent_messages(group["id"])

    if not recent_messages:
        await message.answer("No messages to analyze yet!")
        return

    reply = generate_reply(recent_messages, user_name)

    # Save the ghost reply as the user's message
    database_save_message(group["id"], user["id"], reply)

    await message.answer(reply)

@router.message()
async def save_message(message: Message):
    # Skip if no text (photos, stickers, etc.)
    if not message.text:
        return

    telegram_id = message.from_user.id
    tele_handle = message.from_user.username
    display_name = message.from_user.first_name

    telegram_chat_id = message.chat.id
    chat_name = message.chat.title

    message_text = message.text

    sender = get_or_create_user(telegram_id, tele_handle, display_name)
    group = get_or_create_group(telegram_chat_id, chat_name)

    if sender and group:
        database_save_message(group["id"], sender["id"], message_text)
        print(f"{message.from_user.first_name}: {message.text}")

