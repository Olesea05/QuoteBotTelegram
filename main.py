import time
from loader import bot
import handlers.default_handlers
from utils.set_bot_commands import set_default_commands
from utils.run_scheduler import start_scheduler
from database.database import initialize_database
from handlers.default_handlers import fallback

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
