import json
import time
import uuid
import hashlib

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Application, MessageHandler

from functionality import convert_seconds_to_time, relative_time


def generate_offline_uuid(username):
    # Prefix the username with "OfflinePlayer:"
    name = "OfflinePlayer:" + username

    # Create an MD5 hash of the "OfflinePlayer:<username>" string
    md5_hash = hashlib.md5(name.encode('utf-8')).hexdigest()

    # Convert the MD5 hash into a UUID format
    offline_uuid = uuid.UUID(md5_hash)

    return str(offline_uuid)


async def start_command(update: Update, context: ContextTypes):
    await update.message.reply_text(text="Hello, I'm a bot from TgB server. I'm giving some stats about players who play on our server."
                                         "If you want to see the information, type /info [username].")

async def register_command(update: Update, context: ContextTypes):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    whitelist_directory = ""
    with open('whitelist_direction.txt') as f:
        whitelist_directory = f.read().strip()

    with open(whitelist_directory) as f:
        json_string = json.loads("".join(f.readlines()))
        f.close()

    all_names = [i['name'] for i in json_string]

    processed_text = text.replace("/register ", "")
    if message_type == "private":
        if text == "":
            await update.message.reply_text(text="You need to type a username after /register command (e.g. /register Notch).")
            return
        # Check if text has spaces
        elif " " in processed_text:
            await update.message.reply_text(text="Username cannot contain spaces.")
            return
        # Special characters
        elif not processed_text.isalnum():
            await update.message.reply_text(text="Username cannot contain special characters.")
            return
        # Check if username is already in the whitelist
        elif processed_text in all_names:
            await update.message.reply_text(text="Username is already in the whitelist.")
            return
        else:
            # Add username to the whitelist
            json_string.append({"name": processed_text, "uuid": generate_offline_uuid(processed_text)})
            with open(whitelist_directory, 'w') as f:
                f.write(json.dumps(json_string, indent=4))
                f.close()
            await update.message.reply_text(text="Username added to the whitelist.")



async def online_command(update: Update, context: ContextTypes):
    with open('stats.json') as f:
        string = "".join(f.readlines())
        f.close()
    json_string = json.loads(string)
    info_str = ""
    for i in json_string:
        if i['is_online']:
            info_str += f"✅ {i['name']} online.\n"
        else:
            info_str += f"❌ {i['name']} offline.\n"
    await update.message.reply_text(text=info_str)

async def info_command(update: Update, context: ContextTypes):
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
    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(CommandHandler("online", online_command))
    app.add_handler(CommandHandler("register", register_command))

    print("Polling...")
    app.run_polling(poll_interval=3)