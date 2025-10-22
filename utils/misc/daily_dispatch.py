from loader import bot
from database.database import get_all_users
from quotes.quote_storage import quote_storage
import uuid
from keyboards.inline.inline_buttons import get_quote_buttons
from api.quote_api import get_random_quote


def send_daily_quote() -> None:
    """
    Рассылает случайную цитату всем пользователям.

    Функция выбирает случайную цитату, сохраняет её в локальное хранилище с уникальным ID,
    затем отправляет эту цитату всем зарегистрированным пользователям бота.

    Возвращаемое значение:
        None
    """

    quote, author = get_random_quote()
    quote_id = str(uuid.uuid4())

    quote_storage[quote_id] = {
        'quote': quote,
        'author': author,
        'user_id': None
    }

    text = '{}\n\n— {}'.format(quote, author)
    markup = get_quote_buttons(quote_id)

    users = get_all_users()
    print('👥 Кол-во пользователей: {}'.format(len(users)))

    for user_id in users:
        try:
            bot.send_message(user_id, text, reply_markup=markup)
        except Exception as exc:
            print('❌ Не удалось отправить сообщение пользователю {}: {}'.format(user_id, exc))