import os
import threading
import asyncio
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# =========================
# CONFIG
# =========================

BOT_TOKEN = "8974572676:AAFiA3Lkk-MZz9ScNafkKqpwkwE9MUs8wR0"

CHANNEL = "@minesaver778"
CHANNEL_LINK = "https://t.me/minesaver778"

# ပို့ပေးမယ့် ဖိုင်နာမည် (GitHub repository ထဲမှာ ဒီနာမည်အတိုင်း ရှိရပါမယ်)
FILE_PATH = "Chunk Mirror.mcaddon"

DELETE_AFTER = 300  # ၅ မိနစ် (စက္ကန့် ၃၀၀)


# =========================
# RENDER WEB SERVICE (Keep Alive)
# =========================

web = Flask(__name__)

@web.route("/")
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web.run(host="0.0.0.0", port=port)


# =========================
# START COMMAND
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL, user_id=user_id)
        if member.status in ["left", "kicked"]:
            await send_join_message(update)
        else:
            await send_and_delete_file(update.message, context, user_id)
    except Exception:
        await send_join_message(update)

async def send_join_message(update):
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("♻️ Try Again", callback_data="check_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = (
        "<i>AERO Pixel Craft</i> channel (ချန်နယ်)ကို အရင်ဆုံး join ပေးပါ။\n"
        "join ပြီးပါက try again ကိုထပ်နှိပ်ပြီးရင် file ရပါပြီ။"
    )
    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )


# =========================
# CHECK JOIN & SEND FILE
# =========================

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL, user_id=user_id)
        
        if member.status in ["member", "administrator", "creator"]:
            await query.message.delete()
            await send_and_delete_file_callback(query, context, user_id)
        else:
            keyboard = [
                [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
                [InlineKeyboardButton("♻️ Try Again", callback_data="check_join")]
            ]
            reply
