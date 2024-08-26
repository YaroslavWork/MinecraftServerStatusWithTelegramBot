import json
import time

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Application, MessageHandler

from functionality import convert_seconds_to_time, relative_time


async def start_command(update: Update, context: ContextTypes):
    await update.message.reply_text(text="Hello, I'm a bot from TgB server. I'm giving some stats about players who play on our server.\n"
                                         "If you want to see the stats, type /stats [username].")


async def stats_command(update: Update, context: ContextTypes):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    if message_type == "private":
        with open('stats.json') as f:
            string = "".join(f.readlines())
            f.close()
        json_string = json.loads(string)
        all_names = [i['name'] for i in json_string]

        processed_text = text.replace("/stats", "")
        if processed_text == "":
            await update.message.reply_text(text="You need to type a username after /stats command (e.g. /stats Notch).")
        elif processed_text[1:] in all_names:
            print(processed_text[1:])
            for i in json_string:
                if i['name'] == processed_text[1:]:
                    info_str = ""
                    if i['is_online']:
                        info_str += f"Player {i['name']} is now online.\n"
                        info_str += f"Live session time: {convert_seconds_to_time(time.time() - i['time'])}\n"
                        info_str += f"All time spent: {convert_seconds_to_time(i['time_spent']+time.time()-i['time'])}\n"
                        info_str += f"Dying: {i['kills']} times\n"
                    else:
                        info_str += f"Player {i['name']} is now offline.\n"
                        info_str += f"Last time online: {relative_time(time.time() - i['time'])} ago\n"
                        info_str += f"All time spent in the game: {convert_seconds_to_time(i['time_spent'])}\n"
                    await update.message.reply_text(text=info_str)
        else:
            await update.message.reply_text(text="Player not found.")


if __name__ == "__main__":
    print("Starting bot...")
    with open('token.txt') as f:
        TOKEN = f.read().strip()
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("stats", stats_command))

    print("Polling...")
    app.run_polling(poll_interval=3)