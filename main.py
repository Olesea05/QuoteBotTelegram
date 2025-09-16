import time
from structure_example.loader import bot
import structure_example.handlers.default_handlers
from structure_example.utils.set_bot_commands import set_default_commands
from structure_example.utils.run_scheduler import start_scheduler
from structure_example.database.database import initialize_database
from structure_example.handlers.default_handlers import fallback

if __name__ == "__main__":
    initialize_database()
    set_default_commands(bot)
    start_scheduler()

    while True:
        try:
            bot.infinity_polling(timeout=60)
        except Exception as exc:
            print(f"Ошибка в polling: {exc}")
            time.sleep(5)