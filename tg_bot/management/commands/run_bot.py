from django.core.management.base import BaseCommand

from tg_bot.bot import main


class Command(BaseCommand):
    """
    Кастомная команда для запуска бота
    """
    help = "Запускает Telegram-бота"

    def handle(self, *args, **kwargs):
        main()
