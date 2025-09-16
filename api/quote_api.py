import os
import requests
from typing import Optional, Tuple, Union


def get_random_quote(category: Optional[str] = None) -> Union[Tuple[str, str], str]:
    """
    Получает случайную цитату с внешнего API.

    Args:
        category (Optional[str]): Категория цитаты. Если None, берётся случайная.

    Returns:
        Union[Tuple[str, str], str]: Кортеж (цитата, автор) или строка с сообщением об ошибке.
    """
    url = "https://api.api-ninjas.com/v1/quotes"
    headers = {"X-Api-Key": os.getenv("RAPID_API_KEY")}
    params = {}

    if category is not None:
        params["category"] = category

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        quote = data[0]["quote"]
        author = data[0]["author"]
        return quote, author
    except Exception as exc:
        return "Ошибка при получении цитаты: {}".format(exc)