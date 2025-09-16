from telebot.types import BotCommand
from structure_example.config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot) -> None:
    """
    Устанавливает список команд по умолчанию для Telegram-бота.

    Args:
        bot: Экземпляр Telegram-бота (обычно `telebot.TeleBot`), для которого нужно
            задать команды, отображаемые при вводе '/' в чате.
    """
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )