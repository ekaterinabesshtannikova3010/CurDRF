import logging
import os

from asgiref.sync import sync_to_async
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler

from user.models import User  # Импортируем модель User

# Загрузка переменных окружения из .env файла
load_dotenv(override=True)

# Настройка логирования для отслеживания работы
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


@sync_to_async
def save_chat_id(chat_id, user_id):
    """
    Функция для сохранения chat_id в базе данных
    """
    try:
        user, created = User.objects.get_or_create(id=user_id)

        if created:
            user.chat_id = chat_id  # Создаем новое поле chat_id
            user.save()
            logger.info(
                f"Created new user with user_id {user_id} and saved chat_id {chat_id}"
            )
        else:
            user.chat_id = chat_id
            user.save()
            logger.info(f"Updated chat_id {chat_id} for existing user {user_id}")
    except Exception as e:
        logger.error(f"Error saving chat_id for user {user_id}: {e}")
        raise e


async def start(update: Update, context):
    """
    Функция для команды "/start"
    """
    try:
        logger.info(f"Received /start command from {update.message.chat.id}")
        # Отправляем сообщение при старте
        await update.message.reply_text("Hello, I am your bot!")

        # Сохраняем chat_id пользователя (в асинхронном контексте)
        await save_chat_id(update.message.chat.id, update.message.from_user.id)

    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await update.message.reply_text("Sorry, something went wrong.")


def main():
    """
    Основная функция для создания бота
    """
    try:
        # Токен вашего бота, полученный от BotFather
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            logger.error("Bot token not found. Please check your .env file.")
            return

        # Создаем приложение бота
        application = Application.builder().token(token).build()

        # Регистрируем обработчики
        application.add_handler(CommandHandler("start", start))

        # Запуск бота
        application.run_polling()

        logger.info("Bot is starting...")
    except Exception as e:
        logger.error(f"Error while starting bot: {e}")


if __name__ == "__main__":
    main()
