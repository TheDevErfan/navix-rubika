import inspect
from typing import Callable, List, Tuple, Any

class Router:
    def __init__(self):
        # ذخیره هندلرها به همراه فیلترهایشان
        self.message_handlers: List[Tuple[Callable, list]] = []

    def message(self, *filters: Any):
        def decorator(func: Callable) -> Callable:
            self.message_handlers.append((func, list(filters)))
            return func
        return decorator

    async def dispatch(self, message_obj_or_text):
        for handler, _ in self.message_handlers:
            if inspect.iscoroutinefunction(handler):
                await handler(message_obj_or_text)
            else:
                handler(message_obj_or_text)
