import unittest
from navix import NavixBot, User, Chat, Message, NavixError

class TestNavixFramework(unittest.TestCase):
    def test_bot_initialization(self):
        bot = NavixBot(token="test_token")
        self.assertEqual(bot.token, "test_token")

    def test_models_creation(self):
        user = User(id="123", username="test_user")
        chat = Chat(id="456", type="group")
        message = Message(message_id="789", text="Hello", author=user, chat=chat)
        
        self.assertEqual(message.author.username, "test_user")
        self.assertEqual(message.chat.type, "group")
        self.assertEqual(message.text, "Hello")

    def test_exceptions(self):
        with self.assertRaises(NavixError):
            raise NavixError("Test error")

if __name__ == "__main__":
    unittest.main()
