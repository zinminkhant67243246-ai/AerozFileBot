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

# ထည့်သွင်းပေးလိုက်သော Bot Token
BOT_TOKEN = "8974572676:AAFiA3Lkk-MZz9ScNafkKqpwkwE9MUs8wR0"

# Channel စာရင်း (Channel 2 ခုလုံးထည့်သွင်းထားသည်)
CHANNELS = [
    ("MineSaver", "@minesaver778"),
    ("ModFile", "@modfile888"),
]

FILE_NAME = "Your_File.mcpack"

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

async def check_joined(user_id, bot):
    for name, channel in CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception:
            return False
    return True

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "File ရယူရန် အောက်ပါ Channel နှစ်ခုစလုံးကို join ပေးပါ။\n"
        "Join ပြီးရင် ♻️ Try Again ကို နှိပ်ပေးပါ။"
    )
    await update.message.reply_text(
        text,
        reply_markup=buttons()
    )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    joined = await check_joined(query.from_user.id, context.bot)

    if not joined:
        await query.message.edit_text(
            "File ရယူရန် Channel အားလုံးကို join ပေးပါ။\n"
            "Join ပြီးမှ Try Again ကို ထပ်နှိပ်ပါ။",
            reply_markup=buttons()
        )
    else:
        await query.message.delete()
        await context.bot.send_document(
            chat_id=query.from_user.id,
            document=FILE_NAME,
            caption="ကျေးဇူးတင်ပါတယ်! သင့်ရဲ့ File ကို ပို့ပေးလိုက်ပါပြီ။"
        )

def main():
    # Flask ကို Background Thread နဲ့ Run ခြင်း (Render / Koyeb စတဲ့ hosting တွေအတွက်)
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
