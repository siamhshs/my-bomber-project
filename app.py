import os
import telebot
from flask import Flask, request

# আপনার নতুন টোকেন
TOKEN = "8417159517:AAEm_AKfZ9YD7v6QHX1aO4QIponpd77FuAA"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# মেইন মেনু বাটন
def main_menu():
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn1 = telebot.types.InlineKeyboardButton("💣 START BOMB", callback_data="start")
    btn2 = telebot.types.InlineKeyboardButton("👥 REFERRAL", callback_data="refer")
    btn3 = telebot.types.InlineKeyboardButton("ℹ️ MY INFO", callback_data="info")
    markup.add(btn1, btn2, btn3)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "💣 **SMS BOMBER PRO**\n━━━━━━━━━━━━━\nবট এখন অনলাইন! আপনার সার্ভিস ব্যবহার করতে নিচের বাটন চাপুন।", 
                     reply_markup=main_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "start":
        bot.send_message(call.message.chat.id, "📞 **টার্গেট নম্বরটি দিন:**")
    elif call.data == "refer":
        bot.send_message(call.message.chat.id, f"🔗 **আপনার আইডি:** {call.from_user.id}\nরেফার লিঙ্ক শীঘ্রই আসছে!")
    elif call.data == "info":
        bot.send_message(call.message.chat.id, f"👤 **ইউজার তথ্য:**\nID: `{call.from_user.id}`\nStatus: Premium")

# Webhook কানেকশন
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # এখানে আপনার Render এর সঠিক URL টি দিন
    bot.set_webhook(url='https://my-bomber-project.onrender.com/' + TOKEN)
    return "<h1>Bot is Live!</h1>", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
