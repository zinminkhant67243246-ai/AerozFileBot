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

BOT_TOKEN = "8938593861:AAGlEgHLBaP7LcyUDvQhPm4sQWdhmCW27nA"

CHANNEL = "@minesaver778"
CHANNEL_LINK = "https://t.me/minesaver778"

# 🛑 User တွေကို ပို့ပေးချင်တဲ့ Link (Channel ထဲက Post Link ဖြစ်စေ, Download Link ဖြစ်စေ ဒီမှာထည့်ပါ)
TARGET_LINK = "https://t.me/minesaver778/your_post_id"

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
            await send_target_link(update)
    except Exception:
        await send_join_message(update)

async def send_join_message(update):
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel 1", url=CHANNEL_LINK)],
        [InlineKeyboardButton("♻️ Try Again", callback_data="check_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "<i>AERO Pixel Craft</i> ရဲ့ ချိန်နယ်ကို အရင် join ပါ join ပြီးရင် Try Agin ကိုထက်နှိပ်ပါ နှိပ်ပြီးရင် ကိုယ့်လူတို့လိုချင်တာရပါပြီ",
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
                await send_target_link_callback(query, context)
        except Exception:
            await query.edit_message_text("❌ Channel စစ်ဆေးရာတွင် အမှားအယွင်းရှိနေပါသည်။ ကျေးဇူးပြု၍ ထပ်ကြိုးစားပါ။")

async def send_target_link(update):
    keyboard = [
        [InlineKeyboardButton("📥 လိုချင်တာယူရန် (Download)", url=TARGET_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "✅ ကျေးဇူးတင်ပါတယ်! သင် Join ပြီးဖြစ်ပါ၍ အောက်ပါခလုတ်ကိုနှိပ်ပြီး ရယူနိုင်ပါပြီ -",
        reply_markup=reply_markup
    )

async def send_target_link_callback(query, context):
    keyboard = [
        [InlineKeyboardButton("📥 လိုချင်တာယူရန် (Download)", url=TARGET_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="✅ ကျေးဇူးတင်ပါတယ်! သင် Join ပြီးဖြစ်ပါ၍ အောက်ပါခလုတ်ကိုနှိပ်ပြီး ရယူနိုင်ပါပြီ -",
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
