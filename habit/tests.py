from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from habit.models import Habit

User = get_user_model()


class HabitModelTest(TestCase):

    def setUp(self):
        """
        Создаем пользователя для использования в тестах.
        """
        self.user = User.objects.create_user(
            email="testuser@example.com", password="password123"
        )

    def test_create_valid_habit(self):
        """
        Тест создания привычки с корректными данными.
        """
        habit = Habit.objects.create(
            user=self.user,
            place="Gym",
            time="08:00",
            action="Workout",
            is_pleasant=False,
            period=3,
            time_to_complete=90,
            is_public=True,
        )
        self.assertEqual(habit.user, self.user)
        self.assertEqual(habit.place, "Gym")
        self.assertEqual(habit.action, "Workout")

    def test_invalid_time_to_complete(self):
        """
        Проверяем валидацию: `time_to_complete` не должен превышать 120.
        """
        habit = Habit(
            user=self.user,
            place="Home",
            time="10:00",
            action="Meditate",
            time_to_complete=150,
        )
        with self.assertRaises(ValidationError) as context:
            habit.clean()
        self.assertIn(
            "The 'time_to_complete' cannot exceed 120 seconds.", str(context.exception)
        )

    def test_invalid_period(self):
        """
        Проверяем валидацию: `period` не должен быть больше 7 дней.
        """
        habit = Habit(
            user=self.user, place="Park", time="06:00", action="Run", period=10
        )
        with self.assertRaises(ValidationError) as context:
            habit.clean()
        self.assertIn("The 'period' cannot exceed 7 days.", str(context.exception))

    def test_invalid_reward_and_related_habit(self):
        """
        Проверяем валидацию: нельзя указать `reward` и `related_habit` одновременно.
        """
        pleasant_habit = Habit.objects.create(
            user=self.user, place="Park", time="07:00", action="Walk", is_pleasant=True
        )
        habit = Habit(
            user=self.user,
            place="Park",
            time="08:00",
            action="Read",
            reward="Book",
            related_habit=pleasant_habit,
        )
        with self.assertRaises(ValidationError) as context:
            habit.clean()
        self.assertIn(
            "Cannot set both 'reward' and 'related_habit'.", str(context.exception)
        )

    def test_pleasant_habit_with_invalid_fields(self):
        """
        Проверяем валидацию: у приятной привычки не может быть `reward` или `related_habit`.
        """
        pleasant_habit = Habit(
            user=self.user,
            place="Cafe",
            time="15:00",
            action="Relax",
            is_pleasant=True,
            reward="Coffee",
        )
        with self.assertRaises(ValidationError) as context:
            pleasant_habit.clean()
        self.assertIn(
            "Pleasant habits cannot have 'reward' or 'related_habit'.",
            str(context.exception),
        )

    def test_related_habit_is_not_pleasant(self):
        """
        Проверяем валидацию: связанные привычки должны быть приятными.
        """
        non_pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Home",
            time="18:00",
            action="Study",
            is_pleasant=False,
        )
        habit = Habit(
            user=self.user,
            place="Library",
            time="19:00",
            action="Read",
            related_habit=non_pleasant_habit,
        )
        with self.assertRaises(ValidationError) as context:
            habit.clean()
        self.assertIn(
            "Only pleasant habits can be set as 'related_habit'.",
            str(context.exception),
        )
