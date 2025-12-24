import os
import telebot
from flask import Flask, request

# আপনার টোকেন
TOKEN = "8522736474:AAEeqI9riuBrlp8sCSOLyVXUtXHkbddru48"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # আপাতত কোনো লক নেই, যে কেউ ব্যবহার করতে পারবে
    welcome_text = (
        f"💣 **SMS BOMBER PRO v7.0**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👋 স্বাগতম, {message.from_user.first_name}!\n"
        f"🆔 আপনার আইডি: `{message.from_user.id}`\n\n"
        f"বটটি এখন কাজ করছে। বোম্বিং শুরু করতে প্রস্তুত?"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://' + request.host + '/' + TOKEN)
    return "<h1>Bot is Active!</h1>", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
