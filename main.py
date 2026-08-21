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

# Bot Token အသစ်
BOT_TOKEN = "8974572676:AAFiA3Lkk-MZz9ScNafkKqpwkwE9MUs8wR0"

CHANNEL = "@minesaver778"
CHANNEL_LINK = "https://t.me/minesaver778"

# Render Web Service အတွက်
web = Flask(__name__)

@web.route("/")
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web.run(host="0.0.0.0", port=port)

# Start Command
async def start(update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL, user_id=user_id)
        if member.status in ["left", "kicked"]:
            await send_join_message(update)
        else:
            await send_file_message(update, context)
    except Exception:
        await send_join_message(update)

async def send_join_message(update):
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("♻️ Try Again", callback_data="check_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "<i>AERO Pixel Craft</i> ရဲ့ Channel ကို အရင် join ပါ။ Join ပြီးရင် Try Again ကို ထပ်နှိပ်ပါ။",
        reply_markup=reply_markup,
        parse_mode="HTML"
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
                await send_file_message_callback(query, context)
        except Exception:
            await query.edit_message_text("❌ Channel စစ်ဆေးရာတွင် အမှားအယွင်းရှိနေပါသည်။")

async def send_file_message(update, context):
    # ဒီနေရာမှာ Bot ဆီကနေ ပို့မယ့် ဖိုင် (Document) ကို ထည့်ပါ
    # ဥပမာ - your_file.mcpack ကို Bot ဆီကို တစ်ခါပို့ပြီး ရလာတဲ့ file_id ကို ဒီမှာ ထည့်နိုင်ပါတယ်
    # ဒါမှမဟုတ် URL (သို့) local file path ကို သုံးနိုင်ပါတယ်
    keyboard = [
        [InlineKeyboardButton("📢 UPDATE CHANNEL", url=CHANNEL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # ဥပမာအနေနဲ့ စာနဲ့ ခလုတ်ကို ပို့ပေးထားပါတယ် (ဖိုင်တိုက်ရိုက်ပို့ချင်ရင် context.bot.send_document သုံးပါ)
    await update.message.reply_text(
        "📂 ဖိုင်ကို အောက်ပါလင့်ခ်မှ ရယူနိုင်ပါသည် -",
        reply_markup=reply_markup
    )

async def send_file_message_callback(query, context):
    keyboard = [
        [InlineKeyboardButton("📢 UPDATE CHANNEL", url=CHANNEL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="✅ ကျေးဇူးတင်ပါတယ်! သင် Join ပြီးဖြစ်ပါ၍ ဖိုင်ကို ရယူနိုင်ပါပြီ -",
        reply_markup=reply_markup
    )

def main():
    t = threading.Thread(target=run_web)
    t.start()
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    application.run_polling()

if __name__ == "__main__":
    main()
