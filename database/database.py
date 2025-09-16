from peewee import (
    SqliteDatabase, Model, IntegerField, TextField, DateTimeField, CompositeKey
)
from datetime import datetime, timedelta
from typing import Optional, List, Tuple

db = SqliteDatabase('database/user_history.db')


class BaseModel(Model):
    """
    Базовая модель с привязкой к базе данных.
    """
    class Meta:
        database = db


class User(BaseModel):
    """
    Модель пользователя.
    """
    user_id: int = IntegerField(primary_key=True)
    username: Optional[str] = TextField(null=True)
    first_seen: datetime = DateTimeField(default=datetime.utcnow)
    last_seen: datetime = DateTimeField(default=datetime.utcnow)


class UserHistory(BaseModel):
    """
    Модель истории команд пользователя.
    """
    user_id: int = IntegerField()
    command: str = TextField()
    timestamp: datetime = DateTimeField(default=datetime.utcnow)


class Favorite(BaseModel):
    """
    Модель избранных цитат.
    """
    user_id: int = IntegerField()
    quote_id: str = TextField()
    quote_text: str = TextField()
    quote_author: str = TextField()

    class Meta:
        primary_key = CompositeKey('user_id', 'quote_id')


def initialize_database() -> None:
    """
    Подключается к базе данных и создаёт таблицы, если их нет.
    """
    if db.is_closed():
        db.connect()
    db.create_tables([User, UserHistory, Favorite])
    db.close()


def add_to_history(user_id: int, command: str) -> None:
    """
    Добавляет команду пользователя в историю запросов.

    Args:
        user_id (int): ID пользователя.
        command (str): Команда, которую пользователь выполнил.
    """
    UserHistory.create(user_id=user_id, command=command)


def get_history(user_id: int) -> List[Tuple[str, str]]:
    """
    Возвращает историю команд пользователя в виде списка кортежей.

    Args:
        user_id (int): ID пользователя.

    Returns:
        List[Tuple[str, str]]: Список кортежей (timestamp, command).
    """
    rows = (UserHistory
            .select(UserHistory.timestamp, UserHistory.command)
            .where(UserHistory.user_id == user_id)
            .order_by(UserHistory.timestamp.desc()))
    return [(row.timestamp.strftime('%Y-%m-%d %H:%M:%S'), row.command) for row in rows]


def add_to_favorites(user_id: int, quote_id: str, quote_text: str, quote_author: str) -> bool:
    """
    Добавляет цитату в избранное для пользователя.

    Args:
        user_id (int): ID пользователя.
        quote_id (str): Уникальный ID цитаты.
        quote_text (str): Текст цитаты.
        quote_author (str): Автор цитаты.

    Returns:
        bool: True, если добавление прошло успешно, False — если цитата уже есть.
    """
    try:
        Favorite.create(
            user_id=user_id,
            quote_id=quote_id,
            quote_text=quote_text,
            quote_author=quote_author
        )
        return True
    except Exception:
        return False


def get_favorites(user_id: int) -> List[Tuple[str, str, str]]:
    """
    Возвращает список избранных цитат пользователя.

    Args:
        user_id (int): ID пользователя.

    Returns:
        List[Tuple[str, str, str]]: Список кортежей (quote_id, quote_text, quote_author).
    """
    quotes = Favorite.select().where(Favorite.user_id == user_id)
    return [(q.quote_id, q.quote_text, q.quote_author) for q in quotes]


def remove_favorite_quote(user_id: int, quote_id: str) -> bool:
    """
    Удаляет цитату из избранного пользователя.

    Args:
        user_id (int): ID пользователя.
        quote_id (str): Уникальный ID цитаты.

    Returns:
        bool: True, если удаление прошло успешно, False если цитата не найдена.
    """
    deleted = Favorite.delete().where(
        (Favorite.user_id == user_id) & (Favorite.quote_id == quote_id)
    ).execute()
    return deleted > 0


def format_timestamp_to_local(timestamp: str) -> str:
    """
    Переводит метку времени UTC в локальное время (UTC+3) и форматирует в строку.

    Args:
        timestamp (str): Время в формате '%Y-%m-%d %H:%M:%S' (UTC).

    Returns:
        str: Локальное время в формате 'дд.мм.гггг ЧЧ:ММ'.
    """
    utc_dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    local_dt = utc_dt + timedelta(hours=3)
    return local_dt.strftime('%d.%m.%Y %H:%M')


def add_or_update_user(user_id: int, username: Optional[str] = None) -> None:
    """
    Добавляет пользователя в базу или обновляет время последнего визита.

    Args:
        user_id (int): ID пользователя.
        username (Optional[str]): Имя пользователя (username).
    """
    user, created = User.get_or_create(user_id=user_id, defaults={'username': username})
    if not created:
        user.username = username
        user.last_seen = datetime.utcnow()
        user.save()


def get_all_users() -> List[int]:
    """
    Возвращает список всех ID пользователей из базы.

    Returns:
        List[int]: Список user_id.
    """
    return [u.user_id for u in User.select()]