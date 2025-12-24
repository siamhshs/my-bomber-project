import os
import telebot
import requests
from flask import Flask, request

# আপনার টোকেন এবং তথ্য
TOKEN = "8475845199:AAHX1diGmHBepMcYc8NSWQeXNVn_r2jBhjI"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ইউজার ডেটা স্টোর
user_dict = {}

# মেইন ড্যাশবোর্ড মেনু
def main_menu(name, user_id):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn1 = telebot.types.InlineKeyboardButton("💣 START BOMB", callback_data="start_bomb")
    btn2 = telebot.types.InlineKeyboardButton("👥 REFERRAL", callback_data="refer")
    btn3 = telebot.types.InlineKeyboardButton("ℹ️ MY INFO", callback_data="info")
    btn4 = telebot.types.InlineKeyboardButton("📢 CHANNEL", url="https://t.me/your_channel")
    markup.add(btn1, btn2, btn3, btn4)
    
    welcome_text = (
        f"💣 **SMS_BLAST_914.0**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👋 স্বাগতম, {name}!\n"
        f"🆔 ইউজার আইডি: `{user_id}`\n\n"
        f"👇 বোম্বিং শুরু করতে নিচের বাটন চাপুন:"
    )
    return welcome_text, markup

@bot.message_handler(commands=['start'])
def start(message):
    text, markup = main_menu(message.from_user.first_name, message.from_user.id)
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "start_bomb":
        msg = bot.send_message(call.message.chat.id, "📞 **টার্গেট নম্বরটি দিন (১১ ডিজিট):**", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_number)
    elif call.data == "refer":
        bot.send_message(call.message.chat.id, f"🔗 **রেফার লিঙ্ক:**\nhttps://t.me/Sms_bomber914_bot?start={call.from_user.id}")
    elif call.data == "info":
        bot.send_message(call.message.chat.id, f"👤 **ইউজার তথ্য**\nআইডি: `{call.from_user.id}`\nস্ট্যাটাস: প্রিমিয়াম\nবোম্বিং সীমা: ১০০")

def process_number(message):
    num = message.text
    if len(num) == 11 and num.isdigit():
        user_dict[message.from_user.id] = {'number': num}
        msg = bot.send_message(message.chat.id, "🔢 **কতগুলো ওটিপি পাঠাতে চান? (সর্বোচ্চ ১০০):**")
        bot.register_next_step_handler(msg, process_amount)
    else:
        bot.send_message(message.chat.id, "❌ ভুল নম্বর! আবার /start দিন।")

def process_amount(message):
    try:
        amt = int(message.text)
        if amt > 100: amt = 100
        num = user_dict[message.from_user.id]['number']
        
        bot.send_message(message.chat.id, f"🚀 `{num}` নম্বরে `{amt}`টি ওটিপি পাঠানো শুরু হচ্ছে...", parse_mode="Markdown")
        
        # এখানে বোম্বিং লজিক (API কল) শুরু হবে
        # আপাতত একটি ডামি লুপ দেওয়া হলো
        bot.send_message(message.chat.id, "✅ বোম্বিং সফলভাবে সম্পন্ন হয়েছে!")
    except:
        bot.send_message(message.chat.id, "❌ সংখ্যা দিন। আবার /start দিন।")

# Render Webhook লজিক (রেন্ডারের জন্য বাধ্যতামূলক)
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # এখানে রেন্ডার আপনার হোস্ট থেকে নিজে থেকেই লিঙ্ক নিয়ে নেবে
    bot.set_webhook(url='https://' + request.host + '/' + TOKEN)
    return "<h1>Server is Running!</h1>", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
