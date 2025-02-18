from user.models import User


def save_chat_id(chat_id, user_id):
    """
    Сохраняет chat_id и user_id в базу данных пользователя.
    """
    try:
        user = User.objects.get(id=user_id)
        user.chat_id = chat_id
        user.save()
    except User.DoesNotExist:
        print(f"User with ID {user_id} does not exist.")
