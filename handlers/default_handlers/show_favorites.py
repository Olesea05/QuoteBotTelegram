from telebot.types import Message
from structure_example.loader import bot
from structure_example.database.database import get_favorites, add_to_history
from structure_example.keyboards.inline.inline_buttons import get_favorite_buttons


@bot.message_handler(commands=['show_favorites'])
def show_favorites(message: Message) -> None:
    """
    Обрабатывает команду /show_favorites:
    - Добавляет команду в историю пользователя
    - Получает список избранных цитат пользователя
    - Отправляет каждую цитату с кнопками управления

    Args:
        message (Message): Объект сообщения от пользователя.
    """
    user_id = message.from_user.id
    add_to_history(user_id, '/show_favorites')

    favorites = get_favorites(user_id)

    if not favorites:
        bot.send_message(message.chat.id, 'У вас пока нет избранных цитат.')
        return

    for quote_id, text, author in favorites:
        bot.send_message(
            message.chat.id,
            "{}\n\n— {}".format(text, author),
            reply_markup=get_favorite_buttons(quote_id)
        )