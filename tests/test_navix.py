import asyncio
import unittest
from navix import Router, MockClient, Filters, MemoryStorage, TextFormatter, Validators, TTLCache

class TestNavixEnterprise(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.router = Router()
        self.client = MockClient()

    async def test_message_routing_and_filters(self):
        called = []

        @self.router.message(Filters.command("start"))
        async def start_handler(msg):
            called.append(msg.text)
            await msg.reply("Welcome!")

        await self.client.feed_message(self.router, text="/start bot")
        self.assertEqual(len(called), 1)
        self.assertEqual(self.client.sent_messages[0]["text"], "Welcome!")

    def test_extensions_100(self):
        slug = TextFormatter.slugify("Navix Enterprise Framework 2026!")
        self.assertEqual(slug, "navix-enterprise-framework-2026")
        self.assertTrue(Validators.is_email("test@navix.io"))
        
        cache = TTLCache(ttl=10)
        cache.set("key", "value")
        self.assertEqual(cache.get("key"), "value")

if __name__ == "__main__":
    unittest.main()
