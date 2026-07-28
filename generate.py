import os

def generate_code_dataset():
    output_filename = "navix_10000_examples.py"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("# Navix Framework - Generated Code Patterns and Templates\n\n")
        f.write("import asyncio\nfrom navix import NavixBot, Message, Router, FSMContext, State, StatesGroup\n\n")
        f.write("bot = NavixBot(token='YOUR_TOKEN')\n\n")
        
        for i in range(1, 10001):
            f.write(f"# Example Template Pattern #{i}\n")
            f.write(f"@bot.command('cmd_{i}')\n")
            f.write(f"async def handler_{i}(message: Message):\n")
            f.write(f"    await message.reply('Executing pattern number {i} successfully.')\n\n")
            
    print(f"Generated {output_filename} with 10,000 code patterns successfully.")

if __name__ == '__main__':
    generate_code_dataset()
