from telebot.types import Message
from loader import bot
from database.database import add_to_history


@bot.message_handler(func=lambda message: True)
def handle_unknown(message: Message) -> None:
    """
    Обработчик для неизвестных команд и сообщений:
    - Сохраняет текст сообщения в историю пользователя
    - Отвечает, что команда не распознана и предлагает помощь

    Args:
        message (Message): Объект входящего сообщения.
    """
    user_id = message.from_user.id
    add_to_history(user_id, message.text)
    bot.reply_to(
        message,
        "Извините, я не понимаю эту команду. Напишите /help для списка доступных команд."
    )