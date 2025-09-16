import os
from dotenv import load_dotenv, find_dotenv
from typing import Tuple

if not find_dotenv():
    exit("Переменные окружения не загружены, т.к. отсутствует файл .env")
else:
    load_dotenv()


BOT_TOKEN: str | None = os.getenv("BOT_TOKEN")
RAPID_API_KEY: str | None = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS: Tuple[Tuple[str, str], ...] = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("quote", "Получить новую цитату"),
    ("show_favorites", "Посмотреть избранные цитаты"),
    ("history", "Посмотреть историю запросов"),
)