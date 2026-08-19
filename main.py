import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = "8974572676:AAFiA3Lkk-MZz9ScNafkKqpwkwE9MUs8wR0"

CHANNEL = "@minesaver778"
CHANNEL_LINK = "https://t.me/minesaver778"

FILE_LINK = "https://your-file-link.com/file.apk"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ I've Joined", callback_data="check_join")]
    ]

    await update.message.reply_text(
        "📦 add-on ရယူရန် အရင်ဆုံး Channel Join လုပ်ပေးပါ။",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        member = await context.bot.get_chat_member(
            CHANNEL,
            query.from_user.id
        )

        if member.status in ["member", "administrator", "creator"]:
            keyboard = [
                [InlineKeyboardButton(
                    "📥 Download File",
                    url=FILE_LINK  # Error ဖြစ်နေတဲ့ နေရာကို ရှင်းလင်းပေးလိုက်ပါပြီ
                )]
            ]

            await query.edit_message_text(
                "✅ Channel Join ဖြစ်ပါတယ်!\n\n"
                "အောက်က Download ခလုတ်ကိုနှိပ်ပြီး add-on ကြည့်ရှုပါ။📥",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        else:
            await query.answer(
                "❌ Channel ကို အရင် Join လုပ်ပါ!",
                show_alert=True
            )

    except Exception:
        await query.answer(
            "❌ Channel Join စစ်လို့မရပါ။ Bot ကို Channel ထဲ Admin ထည့်ထားပါ။",
            show_alert=True
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_join, pattern="^check_join$"))

print("Bot is running...")
app.run_polling()
