import asyncio
import time

import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = ''
with open('token.txt') as f:
    TOKEN = f.read().strip()

BOT_USERNAME = "@minecraft_server_TgBbot"
CHAT_ID = "@TgB_server"

log_directory = ''
with open('direction.txt') as f:
    log_directory = f.read()[:-1]

last_line_number = 0


async def send_message(bot):
    global last_line_number
    # Odczytaj zawartość pliku
    file_text = await asyncio.to_thread(read_log_file)
    last_lines = ""
    cur_line_number = last_line_number - 0
    for i in range(last_line_number, len(file_text)):
        cur_line_number += 1
        last_lines += file_text[i]

    if last_lines:
        await bot.send_message(chat_id=CHAT_ID, text=f"{last_lines}")
    last_line_number = len(file_text)

def read_log_file():
    with open(log_directory) as f:
        return f.readlines()


async def main():
    bot = telegram.Bot(token = TOKEN)
    while True:
        try:
            await send_message(bot)
        except Exception as e:
            print(e)
            await asyncio.sleep(0.1)
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
