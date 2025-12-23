import telebot
from telebot import types
import os
import threading
from flask import Flask

# ১. ফ্লস্ক (Flask) সার্ভার সেটআপ (Render এর পোর্টের জন্য)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running Online! 🚀"

# ২. টেলিগ্রাম বট সেটআপ
BOT_TOKEN = "8417159517:AAEKrjhHQMncuvBcZgnQl368nz4sgNF9uY4"
bot = telebot.TeleBot(BOT_TOKEN)

# ইউজার ডেটা স্টোর
user_data = {}

# মেইন মেনু ফাংশন
def show_main_menu(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    
    # ইউজার ডেটা না থাকলে তৈরি করা
    if user_id not in user_data:
        user_data[user_id] = {'total_bombs': 0, 'refer_count': 0, 'last_number': "None"}
    
    welcome_text = (
        f"💣 **sms bomber**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👋 **WELCOME, {name}!**\n"
        f"🆔 **USER ID:** `{user_id}`\n\n"
        f"👇 **SELECT AN OPTION:**"
    )
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("💣 START BOMB", callback_data="start_bomb")
    btn2 = types.InlineKeyboardButton("👥 REFERRAL", callback_data="referral")
    btn3 = types.InlineKeyboardButton("ℹ️ MY INFO", callback_data="my_info")
    
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# /start কমান্ড
@bot.message_handler(commands=['start'])
def send_welcome(message):
    show_main_menu(message)

# বাটন ক্লিক হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    if call.data == "start_bomb":
        msg = bot.send_message(chat_id, "📞 **Target নম্বরটি দিন (যেমন: 017xxx):**", 
                         reply_markup=back_button())
        bot.register_next_step_handler(msg, get_number)

    elif call.data == "referral":
        refer_link = f"https://t.me/Sms_bomber914_bot?start={user_id}"
        bot.send_message(chat_id, f"🔗 **আপনার রেফার লিঙ্ক:**\n`{refer_link}`", 
                         reply_markup=back_button())

    elif call.data == "my_info":
        data = user_data.get(user_id, {'total_bombs': 0, 'refer_count': 0, 'last_number': "None"})
        info = (f"👤 **MY INFO**\n━━━━━━━━━━\n"
                f"🔢 Last Number: {data['last_number']}\n"
                f"🔥 Total Bombed: {data['total_bombs']}\n"
                f"👥 Total Refer: {data['refer_count']}")
        bot.send_message(chat_id, info, reply_markup=back_button())

    elif call.data == "back":
        bot.delete_message(chat_id, call.message.message_id)
        show_main_menu(call)

# নম্বর নেওয়ার ফাংশন
def get_number(message):
    if not message.text or message.text == "/start": return
    user_data[message.from_user.id]['temp_num'] = message.text
    msg = bot.send_message(message.chat.id, "🔢 **কতগুলো (Amount) ওটিপি পাঠাতে চান?**", 
                     reply_markup=back_button())
    bot.register_next_step_handler(msg, get_amount)

# অ্যামাউন্ট নেওয়ার ফাংশন
def get_amount(message):
    if not message.text or message.text == "/start": return
    user_id = message.from_user.id
    user_data[user_id]['temp_count'] = message.text
    
    num = user_data[user_id]['temp_num']
    amt = user_data[user_id]['temp_count']
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ CONFIRM", callback_data="confirm_bomb"))
    markup.add(types.InlineKeyboardButton("🔙 BACK", callback_data="back"))
    
    bot.send_message(message.chat.id, f"⚠️ **CONFIRMATION**\n\nTarget: {num}\nAmount: {amt}\n\nআপনি কি শুরু করতে চান?", 
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "confirm_bomb")
def confirm_bomb(call):
    user_id = call.from_user.id
    num = user_data[user_id].get('temp_num', "N/A")
    amt = int(user_data[user_id].get('temp_count', 0))
    
    user_data[user_id]['total_bombs'] += amt
    user_data[user_id]['last_number'] = num
    
    bot.edit_message_text(f"🚀 {num} নম্বরে বোম্বিং শুরু হয়েছে...", call.message.chat.id, call.message.message_id)

def back_button():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 BACK", callback_data="back"))
    return markup

# ৩. বট এবং সার্ভার রান করা
if __name__ == "__main__":
    # বটকে আলাদা থ্রেডে চালানো
    threading.Thread(target=lambda: bot.infinity_polling(timeout=10, long_polling_timeout=5)).start()
    
    # ফ্লস্ক সার্ভার রান করা
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
