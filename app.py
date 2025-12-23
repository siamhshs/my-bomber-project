import os
import telebot
from flask import Flask, request

# আপনার দেওয়া টোকেন
TOKEN = "8417159517:AAEKrjhHQMncuvBcZgnQl368nz4sgNF9uY4"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# ১. মেইন ড্যাশবোর্ড বাটন তৈরি
def main_menu():
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn1 = telebot.types.InlineKeyboardButton("💣 START BOMB", callback_data="start_bomb")
    btn2 = telebot.types.InlineKeyboardButton("👥 REFERRAL", callback_data="referral")
    btn3 = telebot.types.InlineKeyboardButton("ℹ️ MY INFO", callback_data="my_info")
    markup.add(btn1, btn2, btn3)
    return markup

# ২. স্টার্ট কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def start(message):
    welcome_msg = (
        f"💣 **sms_boomber**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👋 **WELCOME, {message.from_user.first_name}!**\n"
        f"🆔 **USER ID:** `{message.from_user.id}`\n\n"
        f"👇 **নিচের বাটন থেকে একটি অপশন বেছে নিন:**"
    )
    bot.send_message(message.chat.id, welcome_msg, reply_markup=main_menu(), parse_mode="Markdown")

# ৩. বাটন ক্লিক হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "start_bomb":
        bot.send_message(call.message.chat.id, "📞 নম্বর এবং পরিমাণ দিতে বোম্বিং শুরু করুন। (API সংযুক্ত করুন)")
    elif call.data == "referral":
        bot.send_message(call.message.chat.id, f"🔗 রেফার লিঙ্ক: https://t.me/Sms_bomber914_bot?start={call.from_user.id}")
    elif call.data == "my_info":
        bot.send_message(call.message.chat.id, f"👤 ইউজার আইডি: {call.from_user.id}")

# ৪. Render-এর জন্য Webhook এবং Flask সেটআপ
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    # এখানে আপনার Render URL টি দিন
    bot.set_webhook(url='https://my-bomber-project.onrender.com/' + TOKEN)
    return "Bot is Active!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
