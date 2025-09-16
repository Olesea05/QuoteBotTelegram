import schedule
import time
from threading import Thread
from structure_example.utils.misc.daily_dispatch import send_daily_quote


def job() -> None:
    """
    Задача для ежедневной рассылки цитаты.
    Вызывается планировщиком.
    """
    print("Запускаем ежедневную рассылку...")
    send_daily_quote()


def run_schedule() -> None:
    """
    Запускает планировщик задач, который ежедневно в 17:05
    запускает функцию job.
    Блокирует поток, постоянно проверяя запланированные задачи.
    """
    schedule.every().day.at("11:11").do(job)  # Локальное время (UTC+3)

    while True:
        schedule.run_pending()
        time.sleep(1)


def start_scheduler() -> None:
    """
    Запускает планировщик в отдельном демоническом потоке,
    чтобы основной поток бота не блокировался.
    """
    scheduler_thread = Thread(target=run_schedule)
    scheduler_thread.daemon = True
    scheduler_thread.start()