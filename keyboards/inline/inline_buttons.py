from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_quote_buttons(quote_id: str) -> InlineKeyboardMarkup:
    """
    Создаёт inline-кнопки для новой цитаты.

    Args:
        quote_id (str): Уникальный идентификатор цитаты.

    Returns:
        InlineKeyboardMarkup: Разметка с кнопками перевода и добавления в избранное.
    """
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text='Перевести на русский',
            callback_data='translate:{}'.format(quote_id)
        ),
        InlineKeyboardButton(
            text='Добавить в избранное ⭐',
            callback_data='add_fav:{}'.format(quote_id)
        )
    )
    return keyboard


def get_favorite_buttons(quote_id: str) -> InlineKeyboardMarkup:
    """
    Создаёт inline-кнопку для удаления избранной цитаты.

    Args:
        quote_id (str): Уникальный идентификатор цитаты.

    Returns:
        InlineKeyboardMarkup: Разметка с кнопкой "Удалить из избранного".
    """
    markup = InlineKeyboardMarkup()
    delete_button = InlineKeyboardButton(
        text='🗑 Удалить из избранного',
        callback_data='delete_fav:{}'.format(quote_id)
    )
    markup.add(delete_button)
    return markup