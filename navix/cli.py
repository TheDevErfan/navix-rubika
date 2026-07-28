import sys
import os

def main():
    if len(sys.argv) < 3 or sys.argv[1] != "new-project":
        print("Navix CLI - Enterprise Bot Scaffold Tool")
        print("Usage: navix new-project <project_name>")
        sys.exit(1)
    
    project_name = sys.argv[2]
    os.makedirs(project_name, exist_ok=True)
    
    bot_code = '''import logging
from navix import Client, Filters, Message

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

bot = Client(token="YOUR_BOT_TOKEN")

@bot.message(Filters.command("start"))
async def start_handler(message: Message):
    await message.reply("سلام! ربات سازمانی Navix با موفقیت راه‌اندازی شد.")

if __name__ == "__main__":
    bot.run()
'''
    with open(os.path.join(project_name, "bot.py"), "w", encoding="utf-8") as f:
        f.write(bot_code)
        
    print(f"پروژه غول‌پیکر '{project_name}' با ساختار استاندارد Navix ایجاد شد!")
    print(f"دستور ورود: cd {project_name} && python bot.py")

if __name__ == "__main__":
    main()
