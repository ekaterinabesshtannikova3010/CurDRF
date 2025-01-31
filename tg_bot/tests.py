import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock

from telegram import Chat, Message, Update, User

from tg_bot.bot import start


class TestTelegramBot(unittest.TestCase):
    def test_start_command(self):
        """
        Тест команды /start.
        """
        mock_update = MagicMock(spec=Update)

        # Мокаем атрибуты Update
        mock_user = User(id=12345, is_bot=False, first_name="TestUser")
        mock_chat = Chat(id=12345, type="private")
        mock_message = MagicMock(spec=Message)
        mock_message.chat = mock_chat
        mock_message.from_user = mock_user
        mock_message.reply_text = (
            AsyncMock()
        )
        mock_update.message = mock_message

        # Создаем event loop для выполнения асинхронного теста
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def async_test():
            await start(mock_update, None)  # Запускаем команду /start
            mock_message.reply_text.assert_called_once_with("Hello, I am your bot!")

        loop.run_until_complete(async_test())


if __name__ == "__main__":
    unittest.main()
