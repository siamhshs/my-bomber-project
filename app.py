import os
import telebot
import threading
from flask import Flask

# ১. বট এবং সার্ভার সেটআপ
TOKEN = "8417159517:AAEKrjhHQMncuvBcZgnQl368nz4sgNF9uY4"
bot = telebot.TeleBot(TOKEN, threaded=True)
app = Flask(__name__)

# ইউজার ডেটা স্টোর করার ডিকশনারি
user_data = {}

# ২. মেইন মেনু বাটন (আপনার স্ক্রিনশটের মতো প্রফেশনাল লেআউট)
def main_menu(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    
    # ডেটা না থাকলে নতুন এন্ট্রি তৈরি করা
    if user_id not in user_data:
        user_data[user_id] = {'total': 0, 'ref': 0, 'last': "None"}
    
    welcome_text = (
        f"💣 **SMS_BOMBER**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👋 **WELCOME, {name}!**\n"
        f"📊 **DASHBOARD:**\n"
        f"💎 **BALANCE:** 50 DIAMONDS\n"
        f"🆔 **USER ID:** `{user_id}`\n"
        f"📅 **JOINED:** 22 December 2025\n"
        f"🚀 **PLAN:** PREMIUM (FREE)\n\n"
        f"👇 **SELECT AN OPTION FROM BELOW:**"
    )

    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn1 = telebot.types.InlineKeyboardButton("💣 START BOMB", callback_data="start_bomb")
    btn2 = telebot.types.InlineKeyboardButton("🎁 REDEEM", callback_data="redeem")
    btn3 = telebot.types.InlineKeyboardButton("💰 DAILY BONUS", callback_data="bonus")
    btn4 = telebot.types.InlineKeyboardButton("🏆 LEADERBOARD", callback_data="leaderboard")
    btn5 = telebot.types.InlineKeyboardButton("👥 REFERRAL", callback_data="referral")
    btn6 = telebot.types.InlineKeyboardButton("ℹ️ MY INFO", callback_data="my_info")
    btn7 = telebot.types.InlineKeyboardButton("🛡️ SAFE LIST", callback_data="safe_list")
    btn8 = telebot.types.InlineKeyboardButton("🔑 API INFO", callback_data="api_info")
    btn9 = telebot.types.InlineKeyboardButton("🆘 HELP", callback_data="help")

    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
    markup.row(btn9)
    return welcome_text, markup

# ৩. /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def send_welcome(message):
    text, markup = main_menu(message)
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

# ৪. বাটন ক্লিক লজিক
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    if call.data == "start_bomb":
        msg = bot.send_message(chat_id, "📞 **টার্গেট নম্বরটি দিন (যেমন: 017...):**")
        bot.register_next_step_handler(msg, process_number)
    
    elif call.data == "referral":
        link = f"https://t.me/Sms_bomber914_bot?start={user_id}"
        bot.send_message(chat_id, f"🔗 **আপনার রেফার লিঙ্ক:**\n`{link}`")
    
    elif call.data == "my_info":
        data = user_data.get(user_id, {'total': 0, 'ref': 0, 'last': "None"})
        info = (f"👤 **MY INFO**\n━━━━━━━━━━\n"
                f"🔢 Last Number: {data['last']}\n"
                f"🔥 Total Bombed: {data['total']}\n"
                f"👥 Total Refer: {data['ref']}")
        bot.send_message(chat_id, info)
    
    elif call.data == "back":
        text, markup = main_menu(call)
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.answer_callback_query(call.id, "এই ফিচারটি শীঘ্রই আসছে!")

# ৫. বোম্বিং স্টেপ-বাই-স্টেপ প্রসেস
def process_number(message):
    user_id = message.from_user.id
    user_data[user_id]['temp_num'] = message.text
    msg = bot.send_message(message.chat.id, "🔢 **কতগুলো (Amount) পাঠাতে চান? (Max: 50):**")
    bot.register_next_step_handler(msg, process_amount)

def process_amount(message):
    user_id = message.from_user.id
    user_data[user_id]['temp_amt'] = message.text
    
    num = user_data[user_id]['temp_num']
    amt = user_data[user_id]['temp_amt']
    
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("✅ CONFIRM", callback_data="confirm_final"))
    markup.add(telebot.types.InlineKeyboardButton("🔙 BACK", callback_data="back"))
    
    bot.send_message(message.chat.id, f"⚠️ **CONFIRMATION**\n\nTarget: {num}\nAmount: {amt}\n\nআপনি কি শুরু করতে চান?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "confirm_final")
def start_attack(call):
    user_id = call.from_user.id
    num = user_data[user_id].get('temp_num', 'Unknown')
    amt = user_data[user_id].get('temp_amt', '0')
    
    # ডেটা সেভ করা
    user_data[user_id]['total'] += int(amt) if amt.isdigit() else 0
    user_data[user_id]['last'] = num
    
    bot.edit_message_text(f"🚀 {num} নম্বরে {amt}টি বোম্বিং শুরু হয়েছে...", call.message.chat.id, call.message.message_id)

# ৬. Render পোর্টের জন্য Flask সার্ভার
@app.route('/')
def home():
    return "Bot is Running Online! 🚀"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # বটকে আলাদা থ্রেডে চালানো
    threading.Thread(target=lambda: bot.infinity_polling(timeout=20)).start()
    # Flask সার্ভার চালানো
    run_flask()
