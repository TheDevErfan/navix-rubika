"""
Advanced Filters for Navix Router
"""
from typing import Union, List

class Command:
    """
    فیلتر تشخیص دستورات ربات (مثل /start یا /help)
    """
    def __init__(self, commands: Union[str, List[str]]):
        if isinstance(commands, str):
            self.commands = [commands.lstrip("/")]
        else:
            self.commands = [cmd.lstrip("/") for cmd in commands]

    async def __call__(self, message) -> bool:
        if not message.text:
            return False
        text = message.text.strip()
        if not text.startswith("/"):
            return False
        cmd_part = text.split()[0].lstrip("/")
        return cmd_part in self.commands

class Text:
    """
    فیلتر تطبیق متن پیام
    """
    def __init__(self, text: str, ignore_case: bool = False):
        self.text = text
        self.ignore_case = ignore_case

    async def __call__(self, message) -> bool:
        if not message.text:
            return False
        msg_text = message.text
        if self.ignore_case:
            return msg_text.lower() == self.text.lower()
        return msg_text == self.text


class Filters:
    """Filter collection container"""
    @staticmethod
    def text(msg):
        return True
    @staticmethod
    def command(cmd):
        return True
