from telegram import Bot
from config import BOT_TOKEN, CHANNEL_ID

bot = Bot(token=BOT_TOKEN)


async def createpost(title, per_hour, img_src):
    message = f"New pool available: {title}\nEarnings per hour: {per_hour}\nImage: {img_src}"
    await bot.send_message(chat_id=CHANNEL_ID, text=message)

