import time
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = 12345678  # my.telegram.org မှ api_id ကို ဒီမှာထည့်ပါ
API_HASH = "your_api_hash"  # my.telegram.org မှ api_hash ကို ဒီမှာထည့်ပါ
BOT_TOKEN = "8177264166:AAHXJ2W9ALLq6qvzPqFWy4PljVtHw9jaoVo"
OWNER_ID = 6408752129  # သင့်ရဲ့ User ID ထည့်ပြီးပါပြီ

app = Client("AeroRulesBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

last_post_time = 0

@app.on_message(filters.channel & ~filters.service)
def check_channel_rules(client: Client, message: Message):
    global last_post_time
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else None
    text = message.text or message.caption or ""

    if not text.startswith("#") and user_id != OWNER_ID:
        client.delete_messages(chat_id, message.id)
        client.send_message(chat_id, "⚠️ စကားပြောလိုပါက ရှေ့မှ `#` ခံပေးပါရန်။ ပို့စ်ကို ဖျက်သိမ်းလိုက်ပါပြီ။")
        return

    current_time = time.time()
    if user_id != OWNER_ID:
        if current_time - last_post_time < 3600:  
            client.delete_messages(chat_id, message.id)
            client.send_message(chat_id, "⚠️ စည်းကမ်းချက်အရ ပို့စ်များကို (၁) နာရီခြားမှသာ တင်ခွင့်ရှိပါသည်။ ပို့စ်ကို ဖျက်လိုက်ပါပြီ။")
            return
        last_post_time = current_time

app.run()
