import os
import telebot
from flask import Flask, request

# আপনার টেলিগ্রাম বট টোকেন
TOKEN = "8417159517:AAEKrjhHQMncuvBcZgnQl368nz4sgNF9uY4"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ইউজার ডেটা সাময়িকভাবে রাখার জন্য
user_dict = {}

# মেইন ড্যাশবোর্ড মেনু
def main_menu():
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn1 = telebot.types.InlineKeyboardButton("💣 START BOMB", callback_data="start")
    btn2 = telebot.types.InlineKeyboardButton("👥 REFERRAL", callback_data="refer")
    btn3 = telebot.types.InlineKeyboardButton("ℹ️ MY INFO", callback_data="info")
    markup.add(btn1, btn2, btn3)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        f"💣 **SMS BOMBER PRO**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👋 স্বাগতম, {message.from_user.first_name}!\n"
        f"🆔 আপনার আইডি: `{message.from_user.id}`\n\n"
        f"👇 নিচের বাটন থেকে বোম্বিং শুরু করুন:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "start":
        msg = bot.send_message(call.message.chat.id, "📞 **টার্গেট নম্বরটি দিন (যেমন: 017...):**", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_number)
    elif call.data == "refer":
        bot.send_message(call.message.chat.id, f"🔗 **আপনার রেফার লিঙ্ক:**\nhttps://t.me/Sms_bomber914_bot?start={call.from_user.id}")
    elif call.data == "info":
        bot.send_message(call.message.chat.id, f"👤 **আপনার তথ্য**\nআইডি: `{call.from_user.id}`\nপয়েন্ট: ৫০\nবোম্বিং: ০", parse_mode="Markdown")

def process_number(message):
    user_dict[message.from_user.id] = {'number': message.text}
    msg = bot.send_message(message.chat.id, "🔢 **কতগুলো ওটিপি পাঠাতে চান? (সর্বোচ্চ ১০০):**", parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_amount)

def process_amount(message):
    user_dict[message.from_user.id]['amount'] = message.text
    num = user_dict[message.from_user.id]['number']
    amt = user_dict[message.from_user.id]['amount']
    
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("✅ CONFIRM", callback_data="confirm_now"))
    bot.send_message(message.chat.id, f"⚠️ **নিশ্চিত করুন**\n\nTarget: `{num}`\nAmount: `{amt}`\n\nআপনি কি এখনই শুরু করবেন?", 
                     reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "confirm_now")
def start_bombing(call):
    bot.edit_message_text("🚀 **বোম্বিং প্রসেস শুরু হয়েছে! সফলভাবে ওটিপি যাচ্ছে...**", call.message.chat.id, call.message.message_id, parse_mode="Markdown")

# Render Webhook লজিক (এটি কোনোভাবেই মিস হবে না)
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # এখানে আপনার Render URL দেওয়া হলো
    bot.set_webhook(url='https://my-bomber-project.onrender.com/' + TOKEN)
    return "<h1>Bot is Online!</h1>", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
