from telebot.types import Message, CallbackQuery
from structure_example.loader import bot
from structure_example.api.quote_api import get_random_quote
from deep_translator import GoogleTranslator
import uuid
from structure_example.database.database import (
    add_to_history,
    add_to_favorites,
    remove_favorite_quote
)
from structure_example.keyboards.inline.inline_buttons import get_quote_buttons
from structure_example.quotes.quote_storage import quote_storage


@bot.message_handler(commands=["quote"])
def send_quote(message: Message) -> None:
    """
    Отправляет случайную цитату пользователю с кнопками.

    Args:
        message (Message): Объект сообщения пользователя.
    """
    add_to_history(message.from_user.id, '/quote')
    quote, author = get_random_quote()
    quote_id = str(uuid.uuid4())
    quote_storage[quote_id] = {"quote": quote, "author": author}

    text = "{}\n\n— {}".format(quote, author)
    markup = get_quote_buttons(quote_id)

    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('translate:'))
def handle_translate(call: CallbackQuery) -> None:
    """
    Обрабатывает запрос на перевод цитаты.

    Args:
        call (CallbackQuery): CallbackQuery от кнопки.
    """
    quote_id = call.data.split(':')[1]
    data = quote_storage.get(quote_id)
    if not data:
        bot.send_message(call.message.chat.id, "Цитата не найдена.")
        return

    try:
        translated_quote = GoogleTranslator(source='en', target='ru').translate(data['quote'])
        translated_author = GoogleTranslator(source='en', target='ru').translate(data['author'])
        bot.send_message(
            call.message.chat.id,
            "{}\n\n— {}".format(translated_quote, translated_author)
        )
    except Exception as e:
        bot.send_message(call.message.chat.id, "Ошибка перевода: {}".format(e))


@bot.callback_query_handler(func=lambda call: call.data.startswith('add_fav:'))
def handle_add_to_favorites(call: CallbackQuery) -> None:
    """
    Добавляет цитату в избранное пользователя.

    Args:
        call (CallbackQuery): CallbackQuery от кнопки.
    """
    quote_id = call.data.split(':')[1]
    user_id = call.from_user.id

    data = quote_storage.get(quote_id)
    if not data:
        bot.send_message(call.message.chat.id, "Цитата не найдена.")
        return

    success = add_to_favorites(user_id, quote_id, data['quote'], data['author'])

    if success:
        bot.answer_callback_query(call.id, '✅ Добавлено в избранное!')
    else:
        bot.answer_callback_query(call.id, '⚠️ Уже добавлено.')


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_fav:'))
def handle_delete_favorite(call: CallbackQuery) -> None:
    """
    Удаляет цитату из избранного и удаляет сообщение с цитатой.

    Args:
        call (CallbackQuery): CallbackQuery от кнопки.
    """
    quote_id = call.data.split(':')[1]
    user_id = call.from_user.id

    removed = remove_favorite_quote(user_id, quote_id)

    if removed:
        bot.answer_callback_query(call.id, text='Цитата удалена из избранного ❌')
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as exc:
            print("Ошибка при удалении сообщения: {}".format(exc))
    else:
        bot.answer_callback_query(call.id, text='Цитата уже удалена или не найдена')