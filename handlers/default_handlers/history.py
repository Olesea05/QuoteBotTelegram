from telebot.types import Message
from structure_example.loader import bot
from structure_example.database.database import get_history, format_timestamp_to_local


@bot.message_handler(commands=['history'])
def send_history(message: Message) -> None:
    """
    Обрабатывает команду /history:
    - Получает последние 10 команд пользователя с отметками времени
    - Форматирует время в локальное
    - Отправляет пользователю историю команд или уведомление об отсутствии истории

    Args:
        message (Message): Объект сообщения от пользователя.
    """
    user_id = message.from_user.id
    history = get_history(user_id)

    if not history:
        bot.reply_to(message, "У вас пока нет истории запросов.")
        return

    text = "📜 Ваша история команд:\n\n"
    for i, (timestamp, command) in enumerate(history[:10], start=1):
        local_time = format_timestamp_to_local(timestamp)
        text += "{}. {} — {}\n".format(i, command, local_time)

    bot.reply_to(message, text)