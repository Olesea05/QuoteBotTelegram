from telebot.types import Message
from loader import bot
from database.database import add_to_history, add_or_update_user


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    """
    Обрабатывает команду /start:
    - Добавляет или обновляет пользователя в базе
    - Сохраняет команду в историю
    - Отправляет приветственное сообщение

    Args:
        message (Message): Объект сообщения от пользователя.
    """
    user_id = message.from_user.id
    username = message.from_user.username

    add_or_update_user(user_id, username)
    add_to_history(user_id, '/start')

    bot.reply_to(message, "Привет, {}!".format(message.from_user.full_name))

    welcome_text = (
        "*Я — Мудрый бот «Quote of the Day».*\n\n"
        "Каждый день я буду присылать тебе цитату дня📆 "
        "Это поможет учить английский, вдохновляясь красивыми и мудрыми словами известных людей.\n\n"
        "Рад помочь тебе сделать день немного лучше!✨\n\n"
        "📌Используй команду /quote, чтобы получить новую цитату прямо сейчас,\n"
        "а чтобы познакомиться со мной лучше, и узнать что ещё я могу, используй команду /help"
    )

    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown')