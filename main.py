import os
import threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Bot Token ကို တိုက်ရိုက်ထည့်သွင်းပေးထားပါသည်
BOT_TOKEN = "8938593861:AAGlEgHLBaP7LcyUDvQhPm4sQWdhmCW27nA"

# သင့်ရဲ့ Channel အချက်အလက်များ
CHANNEL = "@minesaver778"
CHANNEL_LINK = "https://t.me/minesaver778"

# Join ပြီးရင် ပို့မယ့်ဖိုင်နာမည် (မိမိပေးလိုသော ဖိုင်နာမည်သို့ ပြောင်းလဲပါ)
FILE_NAME = "Your_File.mcpack"

# Render Web Service အတွက်
web = Flask(__name__)

@web.route("/")
def home():
    return "Bot is running!"

def run_web():
    web.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# Start Command
async def start(update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Check if user joined the channel
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL, user_id=user_id)
        if member.status in ["left", "kicked"]:
            await send_join_message(update)
        else:
            await send_file(update)
    except Exception:
        await send_join_message(update)

async def send_join_message(update):
    keyboard = [
        [InlineKeyboardButton("📢 Channel Join ရန်", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ Join ပြီးပါပြီ", callback_data="check_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "ကျေးဇူးပြု၍ ပထမဦးစွာ ကျွန်ုပ်တို့၏ Channel ကို Join ပေးပါ။ ပြီးမှ အောက်ပါ ခလုတ်ကို နှိပ်ပါ -",
        reply_markup=reply_markup
    )

async def button_callback(update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if query.data == "check_join":
        try:
            member = await context.bot.get_chat_member(chat_id=CHANNEL, user_id=user_id)
            if member.status in ["left", "kicked"]:
                await query.edit_message_text("❌ ကျေးဇူးပြု၍ Channel ကို အရင် Join ပေးပါ။")
            else:
                await query.message.delete()
                await send_file_callback(query, context)
        except Exception:
            await query.edit_message_text("❌ Channel စစ်ဆေးရာတွင် အမှားအယွင်းရှိနေပါသည်။ ကျေးဇူးပြု၍ ထပ်ကြိုးစားပါ။")

async def send_file(update):
    if os.path.exists(FILE_NAME):
        await update.message.reply_document(document=open(FILE_NAME, "rb"), caption="ကျေးဇူးတင်ပါတယ်! ဤသည်မှာ သင်တောင်းဆိုထားသော ဖိုင်ဖြစ်ပါသည်။")
    else:
        await update.message.reply_text("⚠️ ဖိုင် ရှာမတွေ့ပါ။ Admin ထံ ဆက်သွယ်ပါ။")

async def send_file_callback(query, context):
    if os.path.exists(FILE_NAME):
        await context.bot.send_document(chat_id=query.message.chat_id, document=open(FILE_NAME, "rb"), caption="ကျေးဇူးတင်ပါတယ်! ဤသည်မှာ သင်တောင်းဆိုထားသော ဖိုင်ဖြစ်ပါသည်။")
    else:
        await context.bot.send_message(chat_id=query.message.chat_id, text="⚠️ ဖိုင် ရှာမတွေ့ပါ။ Admin ထံ ဆက်သွယ်ပါ။")

def main():
    # Flask ကို Background Thread ဖြင့် Run ရန်
    t = threading.Thread(target=run_web)
    t.start()
    
    # Telegram Bot Application တည်ဆောက်ခြင်း
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Bot စတင်ခြင်း
    application.run_polling()

if __name__ == "__main__":
    main()
