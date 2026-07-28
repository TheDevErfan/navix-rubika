import inspect

class Router:
    def __init__(self):
        self.handlers = []

    def message(self, *args, **kwargs):
        def decorator(func):
            self.handlers.append(func)
            return func
        return decorator

    async def dispatch(self, message_obj_or_text):
        for handler in self.handlers:
            if inspect.iscoroutinefunction(handler):
                await handler(message_obj_or_text)
            else:
                handler(message_obj_or_text)
