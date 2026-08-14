from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Join Channel 1", url="https://t.me/YOUR_CHANNEL_1"),
            InlineKeyboardButton("Join Channel 2", url="https://t.me/YOUR_CHANNEL_2")
        ],
        [
            InlineKeyboardButton("Join Channel 3", url="https://t.me/YOUR_CHANNEL_3"),
            InlineKeyboardButton("Join Channel 4", url="https://t.me/YOUR_CHANNEL_4")
        ],
        [
            InlineKeyboardButton("Join Channel 5", url="https://t.me/YOUR_CHANNEL_5")
        ],
        [
            InlineKeyboardButton("♻️ Try Again", callback_data="try_again")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "ကိုယ့်လူရေ Add-on နဲ့ အခြားအရာတွေ ဒေါင်းဖို့ဆိုရင် Bot က Join ခိုင်းတဲ့ Channel တွေကိုအရင် Join ပြီးရင် Try Again ပြန်နှိပ်လိုက်ရင် File ပေါ်လာမှာပါဗျ။", 
        reply_markup=reply_markup
    )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "try_again":
        await query.edit_message_text(text="ကျေးဇူးတင်ပါတယ်! ဖိုင်ကို ပို့ပေးနေပါပြီ။")

if __name__ == "__main__":
    token = "8228969998:AAEBi9oMn-VA6MATmj8dvCoTVdnM7uryHCw"
    app = ApplicationBuilder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    
    print("Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    app.run_polling()
