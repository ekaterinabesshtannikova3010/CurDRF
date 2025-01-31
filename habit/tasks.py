from celery import shared_task
from django.conf import settings
from telegram import Bot

from user.models import User

from .models import Habit


@shared_task
def send_habit_reminder(user_id, habit_id):
    """
    Напоминание о привычках
    """
    habit = Habit.objects.get(id=habit_id)
    """
    Получаем chat_id пользователя
    """
    chat_id = User.objects.get(id=user_id).chat_id
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

    """
    Отправляем уведомление о привычке
    """
    bot.send_message(chat_id, f"Напоминание: выполните привычку: {habit.name}")
