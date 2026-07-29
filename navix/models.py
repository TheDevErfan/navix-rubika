"""Navix Rubika Framework - Data Models."""

class User:
    """Represents a Rubika user."""
    def __init__(self, id: str = None, username: str = None, **kwargs):
        self.id = id
        self.username = username
        self.extra = kwargs


class Chat:
    """Represents a Rubika chat/group/channel."""
    def __init__(self, id: str = None, type: str = None, **kwargs):
        self.id = id
        self.type = type
        self.extra = kwargs


class Message:
    """Represents a message in Rubika."""
    def __init__(
        self,
        message_id: str = None,
        text: str = None,
        author: User = None,
        chat: Chat = None,
        **kwargs
    ):
        self.message_id = message_id
        self.text = text
        self.author = author
        self.chat = chat
        self.extra = kwargs

    async def reply(self, text: str) -> None:
        """Reply to the current message."""
        pass
