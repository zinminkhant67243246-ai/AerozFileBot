import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging setup
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# တောင်းဆိုထားတဲ့ Bot Token နှင့် Channel Username ကို ထည့်သွင်းထားပါပြီ
TOKEN = "8974572676:AAFiA3Lkk-MZz9ScNafkKqpwkwE9MUs8wR0"
CHANNEL_USERNAME = "@minesaver778"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # User Channel Join ပြီးပြီလား စစ်ဆေးရန် (Force Subscribe logic)
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ["left", "kicked"]:
            await ask_to_join(update)
            return
    except Exception:
        await ask_to_join(update)
        return

    await update.message.reply_text("မင်္ဂလာပါ! ကျေးဇူးပြု၍ လိုချင်သော File သို့မဟုတ် Link ကို ပို့ပေးပါ။")

async def ask_to_join(update: Update):
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')} ")],
        [InlineKeyboardButton("🔄 Try Again", callback_data="check_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = "အောက်မှာပြထားတဲ့ Channel လေးတွေကို join ပြီးရင် Try Again ပြန်နှိပ်လိုက်ပါမှ လိုချင်တဲ့ File, Link တွေကို ပို့ပေးမှာပါဗျ။"
    
    if update.message:
        await update.message.reply_text(msg, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text(msg, reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "check_join":
        user_id = update.effective_user.id
        try:
            member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
            if member.status in ["left", "kicked"]:
                await query.answer("ကျေးဇူးပြု၍ Channel ကို အရင် Join ပေးပါ။", show_alert=True)
            else:
                await query.message.edit_text("ကျေးဇူးတင်ပါတယ်! ယခု Bot ကို အသုံးပြုနိုင်ပါပြီ။ /start ကို ထပ်နှိပ်ပါ။")
        except Exception:
            await query.answer("Channel Join မှု ရှိမရှိ စစ်ဆေး၍မရပါ။", show_alert=True)

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    
    # Bot ကို စတင် Run ခြင်း
    application.run_polling()

if __name__ == "__main__":
    main()
