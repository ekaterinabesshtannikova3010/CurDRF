from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Habit(models.Model):
    """
    Создание модели привычек
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habit"
    )
    place = models.CharField(max_length=100)
    time = models.TimeField()
    action = models.CharField(max_length=50)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={"is_pleasant": True},
        related_name="linked_habit",
    )
    reward = models.CharField(max_length=255, blank=True, null=True)
    period = models.PositiveIntegerField(default=1)
    time_to_complete = models.PositiveIntegerField(default=120)
    is_public = models.BooleanField(default=False)

    def clean(self):
        """
        Проверка: нельзя одновременно указать `reward` и `related_habit`
        """
        if self.reward and self.related_habit:
            raise ValidationError(
                "Cannot set both 'reward' and 'related_habit'. Choose only one."
            )

        # Проверка: `time_to_complete` не должен превышать 120 секунд
        if self.time_to_complete > 120:
            raise ValidationError("The 'time_to_complete' cannot exceed 120 seconds.")

        # Проверка: `period` не должен быть больше 7 дней
        if self.period > 7:
            raise ValidationError("The 'period' cannot exceed 7 days.")

        # Проверка: связанные привычки должны быть приятными
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Only pleasant habits can be set as 'related_habit'.")

        # Проверка: у приятной привычки не может быть `reward` или `related_habit`
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError(
                "Pleasant habit cannot have 'reward' or 'related_habit'."
            )

    def save(self, *args, **kwargs):
        self.clean()  # Вызываем метод clean перед сохранением
        super().save(*args, **kwargs)
