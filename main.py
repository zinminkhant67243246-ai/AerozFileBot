import os
from flask import Flask
from threading import Thread

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# သင့်ရဲ့ Bot Token
BOT_TOKEN = "8974572676:AAFiA3Lkk-MZz9ScNafkKqpwkwE9MUs8wR0"

# Channel စာရင်း
CHANNELS = [
    ("MineSaver", "@minesaver778"),
    ("ModFile", "@modfile888"),
]

# ဥပမာ - Link ကနေ ဝင်လာရင် ပို့ပေးမယ့် ဖိုင်
FILE_NAME = "Your_File.mcpack"

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# User က Channel တွေ join ပြီးပြီလား စစ်ဆေးသည့် function
async def check_joined(user_id, bot):
    for name, channel in CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception:
            return False
    return True

# Channel Join ရမယ့် ခလုတ်များ
def buttons():
    keyboard = [
        [
            InlineKeyboardButton(
                "Join MineSaver ↗",
                url="https://t.me/minesaver778"
            ),
            InlineKeyboardButton(
                "Join ModFile ↗",
                url="https://t.me/modfile888"
            ),
        ],
        [
            InlineKeyboardButton(
                "♻️ Try Again",
                callback_data="check_join"
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# /start နဲ့ ဝင်လာတဲ့အခါ (Link ကနေဖြစ်စေ၊ ပုံမှန်ဖြစ်စေ) စစ်ဆေးခြင်း
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bot = context.bot

    # Channel တွေ join ပြီးပြီလား အရင်စစ်မယ်
    joined = await check_joined(user_id, bot)

    if not joined:
        # မ join ရသေးရင် Channel Join ခိုင်းတဲ့ စာနဲ့ ခလုတ်ပဲ ပြမယ် (ဖိုင်မပို့ပါ)
        text = (
            "⚠️ ဖိုင်ကို ရယူရန် အောက်ပါ Channel နှစ်ခုစလုံးကို အရင် join ပေးပါ။\n\n"
            "Join ပြီးရင် ♻️ Try Again ကို နှိပ်ပါ။"
        )
        await update.message.reply_text(text, reply_markup=buttons())
    else:
        # Join ပြီးသားဆိုရင် ဖိုင်ကို ပို့ပေးမယ်
        args = context.args
        if args:
            file_code = args[0] # Link ထဲပါလာတဲ့ code ကို ယူသုံးလို့ရပါတယ်
            
        await update.message.reply_document(
            document=FILE_NAME,
            caption="ကျေးဇူးတင်ပါတယ်! သင်တောင်းဆိုထားတဲ့ File ကို ပို့ပေးလိုက်ပါပြီ။"
        )

# Try Again ခလုတ်နှိပ်တဲ့အခါ စစ်ဆေးမည့် function
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    joined = await check_joined(user_id, context.bot)

    if not joined:
        await query.message.edit_text(
            "❌ Channel တွေ အားလုံးကို မ join ရသေးပါဘူး။\n"
            "Channel တွေ join ပြီးမှ Try Again ကို ထပ်နှိပ်ပါ။",
            reply_markup=buttons()
        )
    else:
        await query.message.delete()
        await context.bot.send_document(
            chat_id=user_id,
            document=FILE_NAME,
            caption="ကျေးဇူးတင်ပါတယ်! သင့်ရဲ့ File ကို ပို့ပေးလိုက်ပါပြီ။"
        )

def main():
    t = Thread(target=run_web)
    t.start()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check, pattern="check_join"))

    application.run_polling()

if __name__ == "__main__":
    main()
