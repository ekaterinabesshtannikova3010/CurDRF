from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Habit
from .pagination import CustomPagination
from .permissions import IsOwnerOrPublicReadOnly
from .serializers import HabitSerializer


class HabitViewSet(ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrPublicReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Пользователь видит свои привычки и публичные привычки.
        Если передан параметр 'public', показываются только публичные привычки.
        """
        if "public" in self.request.query_params:
            # Если запрос содержит параметр 'public', возвращаем только публичные привычки
            return Habit.objects.filter(is_public=True)

        # По умолчанию возвращаем привычки текущего пользователя и публичные
        return Habit.objects.filter(is_public=True) | Habit.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        """
        При создании привычки автоматически связываем ее с текущим пользователем.
        """
        serializer.save(user=self.request.user)
