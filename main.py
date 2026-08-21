import asyncio
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

FILE_PATH = "Chunk Mirror.mcaddon"

DELETE_AFTER = 300  # 5 minutes


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "🔄 Join Channel 1",
                url=CHANNEL_LINK
            )
        ],
        [
            InlineKeyboardButton(
                "♻️ Try Again",
                callback_data="check_join"
            )
        ]
    ]

    text = (
        "♻️ ကျေးဇူးပြုပြီး အရင်ဆုံး Channel ကို Join ပါ။\n\n"
        "Join ပြီးရင် ♻️ Try Again ကိုနှိပ်ပါ။"
    )

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================
# CHECK JOIN
# =========================

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    try:
        member = await context.bot.get_chat_member(
            CHANNEL,
            user_id
        )

        if member.status in ["member", "administrator", "creator"]:

            await query.edit_message_text(
                "✅ Channel Join ပြီးပါပြီ။\n"
                "📦 File ပို့နေပါတယ်..."
            )

            # Send file
            message = await context.bot.send_document(
                chat_id=user_id,
                document=open(FILE_PATH, "rb"),
                caption=(
                    "📦 File ရပါပြီ။\n\n"
                    "⚠️ ဒီ File Message ကို 5 မိနစ်နောက် "
                    "အလိုအလျောက်ဖျက်ပါမယ်။"
                )
            )

            # Delete after 5 minutes
            await asyncio.sleep(DELETE_AFTER)

            try:
                await context.bot.delete_message(
                    chat_id=user_id,
                    message_id=message.message_id
                )
            except Exception:
                pass

        else:

            keyboard = [
                [
                    InlineKeyboardButton(
                        "🔄 Join Channel 1",
                        url=CHANNEL_LINK
                    )
                ],
                [
                    InlineKeyboardButton(
                        "♻️ Try Again",
                        callback_data="check_join"
                    )
                ]
            ]

            await query.edit_message_text(
                "❌ Channel ကို မ Join ရသေးပါ။\n"
                "အရင် Join ပြီးမှ Try Again နှိပ်ပါ။",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    except Exception as e:

        await query.edit_message_text(
            "⚠️ Channel Join စစ်လို့မရပါ။\n\n"
            "Bot ကို Channel ထဲမှာ Admin ထည့်ထားတာ သေချာစစ်ပါ။"
        )

        print("ERROR:", e)


# =========================
# MAIN
# =========================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(
            check_join,
            pattern="^check_join$"
        )
    )

    print("🤖 Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()
