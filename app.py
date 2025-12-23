import os
import telebot
from flask import Flask, request

# আপনার টোকেন এবং বট সেটআপ
TOKEN = "8417159517:AAEKrjhHQMncuvBcZgnQl368nz4sgNF9uY4"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# ইউজার ডেটা স্টোর
user_data = {}

# মেইন মেনু বাটন ফাংশন
def get_main_menu(name, user_id):
    welcome_text = (
        f"💣 **BOMBER MASTER PRO**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👋 **WELCOME, {name}!**\n"
        f"🆔 **USER ID:** `{user_id}`\n\n"
        f"👇 **একটি অপশন সিলেক্ট করুন:**"
    )
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn1 = telebot.types.InlineKeyboardButton("💣 START BOMB", callback_data="start_bomb")
    btn2 = telebot.types.InlineKeyboardButton("👥 REFERRAL", callback_data="referral")
    btn3 = telebot.types.InlineKeyboardButton("ℹ️ MY INFO", callback_data="my_info")
    markup.add(btn1, btn2, btn3)
    return welcome_text, markup

# কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def start(message):
    text, markup = get_main_menu(message.from_user.first_name, message.from_user.id)
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

# বাটন ক্লিক হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "start_bomb":
        msg = bot.send_message(call.message.chat.id, "📞 **টার্গেট নম্বরটি দিন:**")
        bot.register_next_step_handler(msg, get_num)
    elif call.data == "referral":
        bot.send_message(call.message.chat.id, f"🔗 রেফার লিঙ্ক: https://t.me/Sms_bomber914_bot?start={call.from_user.id}")
    elif call.data == "my_info":
        bot.send_message(call.message.chat.id, f"👤 আপনার আইডি: {call.from_user.id}\n🔥 মোট বোম্বিং: ০")

def get_num(message):
    user_data[message.from_user.id] = {'num': message.text}
    msg = bot.send_message(message.chat.id, "🔢 **কতগুলো ওটিপি পাঠাতে চান?**")
    bot.register_next_step_handler(msg, get_amt)

def get_amt(message):
    num = user_data[message.from_user.id]['num']
    amt = message.text
    bot.send_message(message.chat.id, f"🚀 {num} নম্বরে {amt}টি বোম্বিং শুরু হচ্ছে...")

# Render-এর জন্য Webhook সেটআপ (এটিই আসল সমাধান)
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://my-bomber-project.onrender.com/' + TOKEN)
    return "Bot is Alive!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
