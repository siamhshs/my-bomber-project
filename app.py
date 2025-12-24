import os
import telebot
from flask import Flask, request

# Apnar dewa notun Token
TOKEN = "8475845199:AAHX1diGmHBepMcYc8NSWQeXNVn_r2jBhjI"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# User Data storage
user_dict = {}

# Main Menu Buttons
def main_menu():
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        telebot.types.InlineKeyboardButton("💣 START BOMB", callback_data="start_bomb"),
        telebot.types.InlineKeyboardButton("👥 REFERRAL", callback_data="refer"),
        telebot.types.InlineKeyboardButton("ℹ️ MY INFO", callback_data="info")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        f"💣 **SMS BOMBER PRO v3.0**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👋 Welcome, {message.from_user.first_name}!\n"
        f"🆔 Your ID: `{message.from_user.id}`\n\n"
        f"👇 Bombing shuru korte niche click korun:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "start_bomb":
        msg = bot.send_message(call.message.chat.id, "📞 **Target number-ti den (e.g. 017...):**", parse_mode="Markdown")
        bot.register_next_step_handler(msg, get_number)
    elif call.data == "refer":
        bot.send_message(call.message.chat.id, f"🔗 **Refer Link:** https://t.me/Sms_bomber914_bot?start={call.from_user.id}")
    elif call.data == "info":
        bot.send_message(call.message.chat.id, f"👤 **ID:** `{call.from_user.id}`\n📊 **Status:** Active")

def get_number(message):
    user_dict[message.from_user.id] = {'number': message.text}
    msg = bot.send_message(message.chat.id, "🔢 **Koto gulo SMS pathate chan? (Max 100):**")
    bot.register_next_step_handler(msg, get_amount)

def get_amount(message):
    num = user_dict[message.from_user.id]['number']
    amt = message.text
    bot.send_message(message.chat.id, f"🚀 Target: {num}\n✅ Amount: {amt}\n\nBombing shuru hochhe... 🔥")

# Render Webhook logic
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # Apnar Render URL thik thakle eita kaj korbe
    bot.set_webhook(url='https://my-bomber-project.onrender.com/' + TOKEN)
    return "<h1>Bot is Online and Ready!</h1>", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
