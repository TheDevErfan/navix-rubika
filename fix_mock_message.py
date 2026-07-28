import os

test_path = "navix/test.py"
test_code = '''import inspect

class MockMessage:
    def __init__(self, text):
        self.text = text

    async def reply(self, text):
        return f"Replied: {text}"

class MockClient:
    async def feed_message(self, router, text, *args, **kwargs):
        msg_obj = text if hasattr(text, "text") else MockMessage(text)

        if hasattr(router, "dispatch"):
            if inspect.iscoroutinefunction(router.dispatch):
                await router.dispatch(msg_obj)
            else:
                router.dispatch(msg_obj)
        elif hasattr(router, "handlers"):
            for handler in router.handlers:
                if inspect.iscoroutinefunction(handler):
                    await handler(msg_obj)
                else:
                    handler(msg_obj)
        return True
'''
with open(test_path, "w", encoding="utf-8") as f:
    f.write(test_code)

# رفع هشدار در router.py هم برای جلوگیری از DeprecationWarning
router_path = "navix/router.py"
router_code = '''import inspect

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
'''
with open(router_path, "w", encoding="utf-8") as f:
    f.write(router_code)

print("✅ متد reply و اصلاحات inspect اعمال شدند.")
