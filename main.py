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

# Channel စာရင်း (Channel တွေရဲ့ Username ကို ဒီမှာ ထည့်ပါ)
CHANNELS = [
    ("MineSaver", "@minesaver778"),
    ("ModFile", "@modfile888"),
]

# ပို့ပေးမယ့် ဖိုင်နာမည် (Hosting ထဲမှာရှိတဲ့ ဖိုင်နာမည်နဲ့ တူရပါမယ်)
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

# /start ခေါ်လိုက်ရင် ပထမဆုံး ပေါ်လာမည့် ပုံစံ (File ချက်ချင်း မပို့ပါ)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "File ရယူရန် အောက်ပါ Channel နှစ်ခုစလုံးကို join ပေးပါ။\n"
        "Join ပြီးရင် ♻️ Try Again ကို နှိပ်ပေးပါ။"
    )
    await update.message.reply_text(
        text,
        reply_markup=buttons()
    )

# Try Again ခလုတ်နှိပ်တဲ့အခါ စစ်ဆေးမည့် function
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    joined = await check_joined(query.from_user.id, context.bot)

    if not joined:
        # Join မပြီးသေးရင် စာသားနဲ့ ခလုတ်ကို ဆက်ပြထားမယ်
        await query.message.edit_text(
            "❌ Channel တွေ အားလုံးကို မ join ရသေးပါဘူး။\n"
            "File ရယူရန် Channel အားလုံးကို join ပြီးမှ Try Again ကို ထပ်နှိပ်ပါ။",
            reply_markup=buttons()
        )
    else:
        # Join ပြီးသွားမှသာ ဖိုင်ကို ပို့ပေးမယ်
        await query.message.delete()
        await context.bot.send_document(
            chat_id=query.from_user.id,
            document=FILE_NAME,
            caption="ကျေးဇူးတင်ပါတယ်! သင့်ရဲ့ File ကို ပို့ပေးလိုက်ပါပြီ။"
        )

def main():
    # Flask Web Server ကို Background Thread နဲ့ Run ခြင်း
    t = Thread(target=run_web)
    t.start()

    # Telegram Bot တည်ဆောက်ခြင်း
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check, pattern="check_join"))

    # Bot စတင်ដំណើរការခြင်း
    application.run_polling()

if __name__ == "__main__":
    main()
