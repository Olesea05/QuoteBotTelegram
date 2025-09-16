from telebot.types import Message
from structure_example.database.database import add_to_history
from structure_example.config_data.config import DEFAULT_COMMANDS
from structure_example.loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message) -> None:
    """
    Обрабатывает команду /help:
    - Сохраняет команду в историю
    - Отправляет список доступных команд с описанием

    Args:
        message (Message): Объект сообщения от пользователя.
    """
    add_to_history(message.from_user.id, '/help')
    text = ["/{} - {}".format(command, desc) for command, desc in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))