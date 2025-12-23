import telebot
from telebot import types

# আপনার বট টোকেন
BOT_TOKEN = "8417159517:AAEKrjhHQMncuvBcZgnQl368nz4sgNF9uY4"
bot = telebot.TeleBot(BOT_TOKEN)

# ইউজার ডেটা স্টোর করার জন্য ডিকশনারি
user_data = {}

# ১. মেইন মেনু ফাংশন
def show_main_menu(chat_id, name, user_id):
    welcome_text = (
        f"💣 **sms_bomber**\n"
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
    bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# ২. স্টার্ট কমান্ড
@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {'total_bombs': 0, 'refer_count': 0, 'last_number': "None"}
    
    show_main_menu(message.chat.id, message.from_user.first_name, user_id)

# ৩. বাটন হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    if call.data == "start_bomb":
        msg = bot.send_message(chat_id, "📞 **Target নম্বরটি দিন (যেমন: 017xxx):**", 
                         reply_markup=back_inline_button())
        bot.register_next_step_handler(msg, get_number)

    elif call.data == "referral":
        # আপনার সঠিক ইউজারনেম @Sms_bomber914_bot এখানে যুক্ত করা হয়েছে
        refer_link = f"https://t.me/Sms_bomber914_bot?start={user_id}"
        bot.send_message(chat_id, f"🔗 **আপনার রেফার লিঙ্ক:**\n`{refer_link}`", 
                         reply_markup=back_inline_button())

    elif call.data == "my_info":
        data = user_data.get(user_id)
        info = (f"👤 **MY INFO**\n━━━━━━━━━━\n"
                f"🔢 Last Number: {data['last_number']}\n"
                f"🔥 Total Bombed: {data['total_bombs']}\n"
                f"👥 Total Refer: {data['refer_count']}")
        bot.send_message(chat_id, info, reply_markup=back_inline_button())

    elif call.data == "back":
        bot.delete_message(chat_id, call.message.message_id)
        show_main_menu(chat_id, call.from_user.first_name, user_id)

# ৪. ইনপুট হ্যান্ডলিং প্রসেস (নম্বর -> অ্যামাউন্ট -> কনফার্ম)
def get_number(message):
    user_id = message.from_user.id
    user_data[user_id]['temp_num'] = message.text
    msg = bot.send_message(message.chat.id, "🔢 **কতগুলো (Amount) মেসেজ পাঠাতে চান?**", 
                     reply_markup=back_inline_button())
    bot.register_next_step_handler(msg, get_amount)

def get_amount(message):
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
    num = user_data[user_id]['temp_num']
    amt = int(user_data[user_id]['temp_count'])
    
    # ডেটা আপডেট করা
    user_data[user_id]['total_bombs'] += amt
    user_data[user_id]['last_number'] = num
    
    bot.edit_message_text(f"🚀 {num} নম্বরে বোম্বিং শুরু হয়েছে...", call.message.chat.id, call.message.message_id)
    # এখানে আপনার ওটিপি পাঠানোর লুপটি যুক্ত করতে পারেন

# ৫. ব্যাক বাটন জেনারেটর
def back_inline_button():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 BACK", callback_data="back"))
    return markup

print("Bot @Sms_bomber914_bot is running...")
bot.infinity_polling()
