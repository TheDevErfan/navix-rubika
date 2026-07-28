from navix import Client, Filters

bot = Client(token="YOUR_BOT_TOKEN")

@bot.message(Filters.command("start"))
async def start_command(message):
    await message.reply("سلام!")

@bot.message(Filters.text)
async def echo_handler(message):
    await message.reply(message.text)

if __name__ == "__main__":
    bot.run()
