from __future__ import annotations
from enum import Enum

class ButtonTypeEnum(Enum):
    SIMPLE = "Simple"
    URL = "Url"
    CALLBACK = "Callback"

class UpdateTypeEnum(Enum):
    MESSAGE = "NewMessage"
    CALLBACK_QUERY = "CallbackQuery"
