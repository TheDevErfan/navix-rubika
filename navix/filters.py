import re
import inspect
from typing import Any, Callable, List, Optional, Union

class Filter:
    def __init__(self, func: Callable):
        self.func = func

    async def __call__(self, event: Any) -> bool:
        if inspect.iscoroutinefunction(self.func):
            return await self.func(event)
        return self.func(event)

    def __and__(self, other: 'Filter') -> 'Filter':
        async def combined(ev):
            return await self(ev) and await other(ev)
        return Filter(combined)

    def __or__(self, other: 'Filter') -> 'Filter':
        async def combined(ev):
            return await self(ev) or await other(ev)
        return Filter(combined)

    def __invert__(self) -> 'Filter':
        async def combined(ev):
            return not await self(ev)
        return Filter(combined)

class Filters:
    @staticmethod
    def text(message) -> bool:
        return bool(getattr(message, "text", None))

    @staticmethod
    def command(commands: Union[str, List[str]]):
        if isinstance(commands, str):
            commands = [commands]
        def func(message) -> bool:
            text = getattr(message, "text", "")
            if not text:
                return False
            for cmd in commands:
                if text.startswith(f"/{cmd}"):
                    return True
            return False
        return Filter(func)

    @staticmethod
    def regex(pattern: str):
        compiled = re.compile(pattern)
        def func(message) -> bool:
            text = getattr(message, "text", "")
            return bool(compiled.search(text))
        return Filter(func)

class StateFilter:
    def __init__(self, *states: Optional[str]):
        self.states = [s.name if hasattr(s, "name") else s for s in states]

    async def __call__(self, event) -> bool:
        client = getattr(event, "client", None)
        if not client or not hasattr(client, "storage"):
            return False
        user_id = getattr(event, "sender_id", None)
        if not user_id:
            return False
        current_state = await client.storage.get_state(user_id)
        if None in self.states and current_state is None:
            return True
        return current_state in self.states
