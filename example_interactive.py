import asyncio
import logging
from navix import Client, Filters, InlineKeyboardBuilder, InlineKeyboardButton, FileStorage, Message, CallbackQuery

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

bot = Client(token="YOUR_BOT_TOKEN")
# استفاده از ذخیره‌سازی پایدار روی فایل
bot.storage = FileStorage("bot_storage.json")

@bot.message(Filters.command("start"))
async def start_command(message: Message):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton("کلیک کنید", callback_data="btn_click"),
        InlineKeyboardButton("وب‌سایت", url="https://example.com")
    )
    builder.adjust(2)
    await message.reply("سلام! گزینه مورد نظر را انتخاب کنید:", reply_markup=builder.as_markup())

@bot.callback_query("btn_click")
async def callback_handler(cb: CallbackQuery):
    await cb.answer("عملیات با موفقیت انجام شد!", show_alert=True)
    await cb.message.edit("شما روی دکمه شیشه‌ای کلیک کردید.")

if __name__ == "__main__":
    bot.run()
