from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели привычек
    """

    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "action",
            "time",
            "place",
            "is_public",
            "reward",
            "time_to_complete",
        ]
        read_only_fields = ["user"]

    def validate(self, data):
        """
        Проверка: нельзя одновременно указать `reward` и `related_habit`
        """
        if data.get("reward") and data.get("related_habit"):
            raise serializers.ValidationError(
                "Cannot set both 'reward' and 'related_habit'. Choose only one."
            )

        """
        Проверка: `time_to_complete` не должен превышать 120 секунд
        """
        if data.get("time_to_complete", 0) > 120:
            raise serializers.ValidationError(
                "The 'time_to_complete' cannot exceed 120 seconds."
            )

        """
        Проверка: `period` не должен быть больше 7 дней
        """
        if data.get("period", 1) > 7:
            raise serializers.ValidationError("The 'period' cannot exceed 7 days.")

        """
        Проверка: связанные привычки должны быть приятными
        """
        related_habit = data.get("related_habit")
        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                "Only pleasant habits can be set as 'related_habit'."
            )

        """
        Проверка: у приятной привычки не может быть `reward` или `related_habit`
        """
        if data.get("is_pleasant") and (
                data.get("reward") or data.get("related_habit")
        ):
            raise serializers.ValidationError(
                "Pleasant habits cannot have 'reward' or 'related_habit'."
            )

        return data
