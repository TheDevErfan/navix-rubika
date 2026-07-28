import logging
from navix import Client, Filters, Message

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

bot = Client(token="CAAFED0FKISMXYDFYOHDPZOLGGQCRVSVHGXZGPLEEGDAMKJDLDMKARRHZMIYJZZN")

@bot.message(Filters.command("start"))
async def start_handler(message: Message):
    await message.reply("سلام! ربات شما با کتابخانه Navix با موفقیت روشن شد و آماده پاسخگویی است.")

@bot.message(Filters.text)
async def text_handler(message: Message):
    await message.reply(f"پیام شما دریافت شد: {message.text}")

if __name__ == "__main__":
    bot.run()
