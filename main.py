import os
import threading

from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = "8974572676:AAFiA3Lkk-MZz9ScNafkKqpwkwE9MUs8wR0"

CHANNEL = "@minesaver778"
CHANNEL_LINK = "https://t.me/minesaver778"

# Render Web Service အတွက်
web = Flask(name)

@web.route("/")
def home():
    return "Bot is running!"


def run_web():
    port = int(os.getenv("PORT", 10000))
    web.run(host="0.0.0.0", port=port)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "Join Channel 1 ↗",
                url=CHANNEL_LINK
            )
        ],
        [
            InlineKeyboardButton(
                "♻️ Try Again",
                callback_data="check"
            )
        ]
    ]

    await update.message.reply_text(
        "Hey Aero Pixel Craft\n\n"
        "Please Join All My Update Channels To Use Me!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        member = await context.bot.get_chat_member(
            CHANNEL,
            query.from_user.id
        )

        if member.status in ["member", "administrator", "creator"]:
            await query.message.reply_text(
                "✅ Joined! ကျေးဇူးတင်ပါတယ်။"
            )

        else:
            await query.answer(
                "❌ Channel ကို အရင် Join လုပ်ပါ!",
                show_alert=True
            )

    except Exception:
        await query.answer(
            "❌ Channel Join မလုပ်ရသေးပါ!",
            show_alert=True
        )


def main():
    threading.Thread(
        target=run_web,
        daemon=True
    ).start()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(
            check,
            pattern="^check$"
        )
    )

    app.run_polling()


if name == "main":
    main()
