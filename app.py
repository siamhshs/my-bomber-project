import telebot
from telebot import types
import os
from flask import Flask, request
import threading

# ১. টেলিগ্রাম বট সেটআপ
BOT_TOKEN = "8417159517:AAEKrjhHQMncuvBcZgnQl368nz4sgNF9uY4"
bot = telebot.TeleBot(BOT_TOKEN, threaded=False) # Render-এ Threaded False রাখা ভালো

# ২. ফ্লস্ক সার্ভার (Render পোর্টের জন্য)
app = Flask(__name__)

@app.route('/')
def index():
    return "SMS Bomber Bot is Running!"

# ৩. বট লজিক এবং ডেটা স্টোর
user_data = {}

def show_main_menu(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    
    if user_id not in user_data:
        user_data[user_id] = {'total_bombs': 0, 'refer_count': 0, 'last_number': "None"}
    
    welcome_text = (
        f"💣 **BOMBER MASTER PRO**\n"
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

@bot.message_handler(commands=['start'])
def start_cmd(message):
    show_main_menu(message)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    if call.data == "start_bomb":
        msg = bot.send_message(chat_id, "📞 **টার্গেট নম্বরটি দিন (যেমন: 017...):**")
        bot.register_next_step_handler(msg, get_number)
    
    elif call.data == "referral":
        link = f"http://t.me/Sms_bomber914_bot?start={user_id}"
        bot.send_message(chat_id, f"🔗 **আপনার রেফার লিঙ্ক:**\n`{link}`")
    
    elif call.data == "my_info":
        data = user_data.get(user_id, {'total_bombs': 0, 'refer_count': 0, 'last_number': "None"})
        info = (f"👤 **INFO**\nTotal Bombed: {data['total_bombs']}\nTotal Refer: {data['refer_count']}")
        bot.send_message(chat_id, info)

def get_number(message):
    user_id = message.from_user.id
    if user_id not in user_data: user_data[user_id] = {}
    user_data[user_id]['temp_num'] = message.text
    msg = bot.send_message(message.chat.id, "🔢 **কতগুলো (Amount) পাঠাতে চান?**")
    bot.register_next_step_handler(msg, get_amount)

def get_amount(message):
    user_id = message.from_user.id
    user_data[user_id]['temp_count'] = message.text
    
    num = user_data[user_id]['temp_num']
    amt = user_data[user_id]['temp_count']
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ CONFIRM", callback_data="confirm_now"))
    bot.send_message(message.chat.id, f"Target: {num}\nAmount: {amt}\n\nশুরু করতে কনফার্ম করুন।", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "confirm_now")
def confirm_now(call):
    bot.edit_message_text("🚀 বোম্বিং প্রসেস শুরু হয়েছে!", call.message.chat.id, call.message.message_id)

# ৪. Render-এ বট চালানোর ফাংশন
def run_bot():
    bot.remove_webhook()
    bot.infinity_polling(timeout=60)

if __name__ == "__main__":
    # বটকে আলাদা থ্রেডে চালানো
    threading.Thread(target=run_bot).start()
    # সার্ভার চালানো
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
