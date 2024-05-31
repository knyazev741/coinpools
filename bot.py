from aiogram import Bot
from config import BOT_TOKEN, CHANNEL_ID

bot = Bot(token=BOT_TOKEN)


async def createpost(title, per_hour, img_src):
    profit_str = per_hour.split()[0]
    profit = float(profit_str)

    bronze_earnings = profit / 10
    silver_earnings = profit
    gold_earnings = profit * 100
    platinum_earnings = profit * 500

    message = (
        f"*New pool available*: {title}\n\n"
        f"*Earnings per hour:*\n"
        f"Platinum: {platinum_earnings} $NOT\n"
        f"Gold: {gold_earnings} $NOT\n"
        f"Silver: {silver_earnings} $NOT\n"
        f"Bronze: {bronze_earnings} $NOT\n\n"
        f"*Subscribe* @coinpools"
    )

    await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')


# Don't forget to close the bot session when done
async def close_bot():
    await bot.session.close()
