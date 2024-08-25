import asyncio
import time
import json

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
        content = set_content(file_text[i])
        if content:
            last_lines += f"{content}\n"

    if last_lines:
        await bot.send_message(chat_id=CHAT_ID, text=f"{last_lines}")
    last_line_number = len(file_text)


def read_log_file():
    with open(log_directory) as f:
        return f.readlines()


def writing_stats(json_string):
    with open('stats.json', 'w') as f:
        f.write(json_string)


def set_content(content):
    with open('stats.json') as f:
        string = "".join(f.readlines())
        f.close()
    json_string = json.loads(string)
    all_names = [i['name'] for i in json_string]

    if "joined the game" in content:
        name = content.split("joined the game")[0].split(" ")[3].strip()
        if name not in all_names:
            json_string.append({"name": name, "is_online": True, "time": time.time(), "advancements": [], "kills": 0})
        else:
            for i in json_string:
                if i['name'] == name:
                    i['is_online'] = True
                    i['time'] = time.time()
        writing_stats(json.dumps(json_string, indent=4))
        return f"{name} joined the game"

    elif "left the game" in content:
        name = content.split("left the game")[0].split(" ")[3].strip()
        for i in json_string:
            if i['name'] == name:
                i['is_online'] = False
                i['time'] = time.time()
        writing_stats(json.dumps(json_string, indent=4))
        return f"{name} left the game"
    elif "lost connection" in content:
        pass

    elif "has made the advancement" in content:
        name = content.split(" ")[3]
        advancement = content.split("has made the advancement ")[1].strip()[1:-1]
        for i in json_string:
            if i['name'] == name:
                i['advancements'].append(advancement)
        writing_stats(json.dumps(json_string, indent=4))
        return f"{name} has made the advancement: {advancement}"

    elif content.split(" ")[3] in all_names:
        name = content.split(" ")[3].strip()
        for i in json_string:
            if i['name'] == name:
                i['kills'] += 1
        writing_stats(json.dumps(json_string, indent=4))
        return f"{name}{content.split(name)[1]}"

    return ""


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
    #print(set_content("[01:30:42] [Server thread/INFO]: Olix left the game"))