import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# သင်ပေးထားသော Bot Token ကို တိုက်ရိုက်ထည့်သွင်းထားပါသည်
TOKEN = "8177264166:AAHXJ2W9ALLq6qvzPqFWy4PljVtHw9jaoVo"

# Rule 2 အရ တားမြစ်လိုသော စကားလုံးများ
BANNED_WORDS = ["18+", "adult", "sex", "porn", "အရွယ်မရောက်သေးသူ"]

async def check_channel_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.channel_post or update.message
    if not message:
        return

    # Rule 4: အခြား Channel / နေရာမှ Forward လုပ်ထားသော ပို့စ်ဖြစ်ပါက ဖျက်မည်
    if message.forward_origin or message.forward_from_chat or message.forward_from:
        try:
            await message.delete()
            logging.info("Rule 4 ချိုးဖောက်သဖြင့် Forward လုပ်ထားသော ပို့စ်ကို ဖျက်လိုက်ပါပြီ။")
            return
        except Exception as e:
            logging.error(f"Forward ပို့စ်ဖျက်ရာတွင် အမှားအယွင်း ရှိသည်: {e}")
            return

    # Rule 2: စာသားများထဲတွင် မသင့်လျော်သော စကားလုံးများ ပါဝင်ခြင်း ရှိမရှိ စစ်ဆေးမည်
    text = message.text or message.caption
    if text:
        text_lower = text.lower()
        for word in BANNED_WORDS:
            if word in text_lower:
                try:
                    await message.delete()
                    logging.info(f"Rule 2 ချိုးဖောက်သဖြင့် ပို့စ်ကို ဖျက်လိုက်ပါပြီ (အကြောင်းပြချက်: '{word}')")
                except Exception as e:
                    logging.error(f"ပို့စ်ဖျက်ရာတွင် အမှားအယွင်း ရှိသည်: {e}")
                break

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, check_channel_rules))
    application.run_polling()

if __name__ == '__main__':
    main()
