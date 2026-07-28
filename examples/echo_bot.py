"""
یک نمونه ربات ساده (Echo Bot) با استفاده از کتابخانه Navix
"""
import asyncio
from navix import Client, Router, Dispatcher, Message

client = Client(token="YOUR_BOT_TOKEN")
router = Router()
dp = Dispatcher(client, router)

@router.message()
async def echo_handler(msg: Message):
    if msg.text:
        print(f"پیام دریافت شد: {msg.text}")
        await msg.reply(f"شما گفتید: {msg.text}")

async def main():
    print("ربات نمونه روشن شد...")
    await dp.start_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("ربات متوقف شد.")
