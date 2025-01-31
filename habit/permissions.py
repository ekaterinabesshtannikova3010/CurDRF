from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrPublicReadOnly(BasePermission):
    """
    Разрешает доступ только владельцам объекта или позволяет читать публичные объекты.
    """

    def has_object_permission(self, request, view, obj):
        # Для безопасных методов (GET, HEAD, OPTIONS) проверяем публичность
        if request.method in SAFE_METHODS:
            return obj.is_public or obj.user == request.user
        # Для небезопасных методов проверяем, что пользователь — владелец
        return obj.user == request.user
