import inspect

class MockMessage:
    def __init__(self, text, client=None):
        self.text = text
        self.client = client

    async def reply(self, text):
        msg_data = {"text": text}
        if self.client and hasattr(self.client, "sent_messages"):
            self.client.sent_messages.append(msg_data)
        return msg_data

class MockClient:
    def __init__(self):
        self.sent_messages = []

    async def feed_message(self, router, text, *args, **kwargs):
        msg_obj = text if hasattr(text, "text") else MockMessage(text, client=self)
        if hasattr(msg_obj, "client"):
            msg_obj.client = self

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
