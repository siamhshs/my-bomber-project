import os
import telebot
from flask import Flask, request

# আপনার বট টোকেন এবং রেন্ডার ইউআরএল
TOKEN = "8417159517:AAEKrjhHQMncuvBcZgnQl368nz4sgNF9uY4"
RENDER_URL = "https://my-bomber-project.onrender.com"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ইউজার ডেটা স্টোর
user_state = {}

# মেইন মেনু জেনারেটর
def main_menu():
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        telebot.types.InlineKeyboardButton("💣 START BOMB", callback_data="start_bomb"),
        telebot.types.InlineKeyboardButton("👥 REFERRAL", callback_data="refer"),
        telebot.types.InlineKeyboardButton("ℹ️ MY INFO", callback_data="info"),
        telebot.types.InlineKeyboardButton("🆘 HELP", callback_data="help")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        f"💣 **BOMBER MASTER PRO v2.0**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👋 স্বাগতম, {message.from_user.first_name}!\n"
        f"🚀 আপনার সার্ভিস এখন অনলাইন এবং লাইভ।\n\n"
        f"👇 নিচে থেকে একটি অপশন বেছে নিন:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "start_bomb":
        msg = bot.send_message(call.message.chat.id, "📞 **টার্গেট নম্বরটি দিন (যেমন: 017...):**", parse_mode="Markdown")
        bot.register_next_step_handler(msg, get_number)
    elif call.data == "refer":
        bot.send_message(call.message.chat.id, f"🔗 **আপনার রেফার লিঙ্ক:**\n{RENDER_URL.replace('onrender.com', 't.me/Sms_bomber914_bot')}?start={call.from_user.id}")
    elif call.data == "info":
        bot.send_message(call.message.chat.id, f"👤 **ইউজার আইডি:** `{call.from_user.id}`\n📊 **স্ট্যাটাস:** একটিভ")

def get_number(message):
    user_state[message.from_user.id] = {'number': message.text}
    msg = bot.send_message(message.chat.id, "🔢 **কতগুলো ওটিপি পাঠাতে চান? (সর্বোচ্চ ৫০):**")
    bot.register_next_step_handler(msg, get_amount)

def get_amount(message):
    user_id = message.from_user.id
    user_state[user_id]['amount'] = message.text
    num = user_state[user_id]['number']
    amt = user_state[user_id]['amount']
    
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("✅ CONFIRM ATTACK", callback_data="confirm_final"))
    bot.send_message(message.chat.id, f"⚠️ **কনফার্মেশন**\n\nটার্গেট: {num}\nপরিমাণ: {amt}\n\nআপনি কি নিশ্চিত?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "confirm_final")
def finish(call):
    bot.edit_message_text("🚀 **বোম্বিং শুরু হয়েছে! ওটিপি পাঠানো হচ্ছে...**", call.message.chat.id, call.message.message_id)

# রেন্ডার এবং টেলিগ্রাম কানেকশন (Webhook)
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + '/' + TOKEN)
    return "<h1>Server is Alive and Bot is Running!</h1>", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
