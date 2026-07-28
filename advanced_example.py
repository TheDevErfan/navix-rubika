import asyncio
import logging
from navix import Client, Router, Filters, StatesGroup, State, BaseMiddleware, Message, CallbackQuery

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 1. تعریف میان‌افزار سفارشی برای ثبت لاگ و احراز هویت رویدادها
class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        sender = getattr(event, 'sender_id', 'Unknown')
        print(f"[Middleware Log] Event triggered by user ID: {sender}")
        return await handler(event, data)

# 2. تعریف زیر-روتر (Sub-router) برای تفکیک بخش مدیریت
admin_router = Router()

@admin_router.message(Filters.command("admin"))
async def admin_panel(message: Message):
    await message.reply("به پنل مدیریت پیشرفته خوش آمدید.")

# 3. تعریف ماشین حالت (FSM) برای ثبت‌نام مرحله‌ای کاربران
class RegisterState(StatesGroup):
    name = State()
    age = State()

# 4. راه‌اندازی کلاینت اصلی فریمورک
bot = Client(token="YOUR_BOT_TOKEN")

# اتصال میان‌افزار و زیر-روتر به کلاینت مرکزی
bot.middleware(LoggingMiddleware())
bot.include_router(admin_router)

@bot.message(Filters.command("start"))
async def start_handler(message: Message):
    await bot.storage.set_state(message.sender_id, RegisterState.name.name)
    await message.reply("سلام! فرآیند ثبت‌نام آغاز شد. لطفاً نام خود را وارد کنید:")

@bot.message(Filters.text)
async def fsm_handler(message: Message):
    user_id = message.sender_id
    current_state = await bot.storage.get_state(user_id)

    if current_state == RegisterState.name.name:
        await bot.storage.set_data(user_id, {"name": message.text})
        await bot.storage.set_state(user_id, RegisterState.age.name)
        await message.reply("نام شما ثبت شد. حالا سن خود را وارد کنید:")
        
    elif current_state == RegisterState.age.name:
        data = await bot.storage.get_data(user_id)
        name = data.get("name")
        age = message.text
        await bot.storage.clear(user_id)
        await message.reply(f"ثبت‌نام با موفقیت کامل انجام شد!\nمشخصات:\nنام: {name}\nسن: {age}")
    else:
        await message.reply(f"پیام عمومی دریافت شد: {message.text}")

if __name__ == "__main__":
    bot.run()
