import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.config import settings
from bot.handlers.general import router as general_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

dp.include_router(general_router)


if __name__ == "__main__":
    logger.info("Бот Запущен")
    try:
        dp.run_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")