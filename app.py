import os
import telebot
from flask import Flask, request

# আপনার নতুন টোকেন
TOKEN = "8522736474:AAEeqI9riuBrlp8sCSOLyVXUtXHkbddru48"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# মেইন ড্যাশবোর্ড মেনু
def main_menu(name, user_id):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn1 = telebot.types.InlineKeyboardButton("💣 START BOMB", callback_data="start_bomb")
    btn2 = telebot.types.InlineKeyboardButton("👥 REFERRAL", callback_data="refer")
    btn3 = telebot.types.InlineKeyboardButton("ℹ️ MY INFO", callback_data="info")
    btn4 = telebot.types.InlineKeyboardButton("📢 CHANNEL", url="https://t.me/your_channel")
    markup.add(btn1, btn2, btn3, btn4)
    
    welcome_text = (
        f"💣 **SMS BOMBER PRO v8.0**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👋 স্বাগতম, {name}!\n"
        f"🆔 ইউজার আইডি: `{user_id}`\n\n"
        f"👇 বোম্বিং শুরু করতে নিচের বাটন চাপুন:"
    )
    return welcome_text, markup

@bot.message_handler(commands=['start'])
def start(message):
    text, markup = main_menu(message.from_user.first_name, message.from_user.id)
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "start_bomb":
        bot.send_message(call.message.chat.id, "📞 **টার্গেট নম্বরটি দিন (যেমন: 017...):**", parse_mode="Markdown")
    elif call.data == "refer":
        bot.send_message(call.message.chat.id, f"🔗 **রেফার লিঙ্ক:**\nhttps://t.me/Sms_bomber914_bot?start={call.from_user.id}")
    elif call.data == "info":
        bot.send_message(call.message.chat.id, f"👤 **ইউজার তথ্য**\nআইডি: `{call.from_user.id}`\nস্ট্যাটাস: একটিভ")

# Render Webhook logic
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://' + request.host + '/' + TOKEN)
    return "<h1>Server is Running with All Texts!</h1>", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
