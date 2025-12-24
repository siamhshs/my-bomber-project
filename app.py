import os
import telebot
from flask import Flask, request

# আপনার দেওয়া নতুন টোকেন এবং তথ্য
TOKEN = "8417159517:AAEm_AKfZ9YD7v6QHX1aO4QIponpd77FuAA"
ADMIN_ID = 6900182564
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ইউজার ডেটা স্টোর করার ডিকশনারি
user_states = {}

# মেইন মেনু জেনারেটর
def get_main_menu(name, user_id):
    welcome_text = (
        f"💣 **SMS BOMBER MASTER PRO**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👋 স্বাগতম, {name}!\n"
        f"🆔 আপনার আইডি: `{user_id}`\n\n"
        f"👇 একটি অপশন সিলেক্ট করুন:"
    )
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn1 = telebot.types.InlineKeyboardButton("💣 START BOMB", callback_data="start_bomb")
    btn2 = telebot.types.InlineKeyboardButton("👥 REFERRAL", callback_data="referral")
    btn3 = telebot.types.InlineKeyboardButton("ℹ️ MY INFO", callback_data="my_info")
    markup.add(btn1, btn2, btn3)
    return welcome_text, markup

# স্টার্ট কমান্ড
@bot.message_handler(commands=['start'])
def start_cmd(message):
    text, markup = get_main_menu(message.from_user.first_name, message.from_user.id)
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

# বাটন ক্লিক হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    if call.data == "start_bomb":
        msg = bot.send_message(chat_id, "📞 **Target নম্বরটি দিন (যেমন: 017...):**", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_num)
    elif call.data == "referral":
        bot.send_message(chat_id, f"🔗 আপনার রেফারেল আইডি: {call.from_user.id}")
    elif call.data == "my_info":
        bot.send_message(chat_id, f"👤 আইডি: {call.from_user.id}\n📊 স্ট্যাটাস: এক্টিভ")

def process_num(message):
    user_states[message.from_user.id] = {'number': message.text}
    msg = bot.send_message(message.chat.id, "🔢 **কতগুলো ওটিপি পাঠাতে চান? (সর্বোচ্চ ১০০):**", parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_amt)

def process_amt(message):
    num = user_states[message.from_user.id]['number']
    amt = message.text
    bot.send_message(message.chat.id, f"🚀 {num} নম্বরে {amt}টি ওটিপি পাঠানো শুরু হচ্ছে...")

# Render এবং Telegram কানেকশন (Webhook)
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # আপনার Render URL টি এখানে দিন
    bot.set_webhook(url='https://my-bomber-project.onrender.com/' + TOKEN)
    return "<h1>Bot is Active!</h1>", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
