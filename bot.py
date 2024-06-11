import logging
from aiogram import Bot
from config import BOT_TOKEN, CHANNEL_ID, LEVEL, ADMIN_ID

bot = Bot(token=BOT_TOKEN)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def send_error_to_admin(error_message):
    try:
        await bot.send_message(chat_id=ADMIN_ID, text=f"Error: {error_message}", parse_mode='Markdown')
        logger.info(f"Sent error message to admin: {error_message}")
    except Exception as e:
        logger.error(f"Failed to send error message to admin: {str(e)}")
    finally:
        await close_bot()

async def createpost(title, per_hour, img_src):
    try:
        profit_str = per_hour.split()[0]
        profit = float(profit_str)

        multipliers = {
            "Bronze": 1,
            "Silver": 10,
            "Gold": 1000,
            "Platinum": 5000
        }

        if LEVEL not in multipliers:
            raise ValueError("Unknown level specified in LEVEL")

        # Define base earnings depending on the level
        base_earnings = profit / multipliers[LEVEL]

        # Calculate earnings for each level
        def format_earnings(earnings):
            if earnings.is_integer():
                return f"{int(earnings)}"
            return f"{earnings}"

        bronze_earnings = format_earnings(base_earnings * multipliers["Bronze"])
        silver_earnings = format_earnings(base_earnings * multipliers["Silver"])
        gold_earnings = format_earnings(base_earnings * multipliers["Gold"])
        platinum_earnings = format_earnings(base_earnings * multipliers["Platinum"])

        message = (
            f"*New pool available*: {title}\n\n"
            f"*$NOT per hour:*\n\n"
            f"▪ Platinum: {platinum_earnings}\n"
            f"▪ Gold: {gold_earnings}\n"
            f"▪ Silver: {silver_earnings}\n"
            f"▪ Bronze: {bronze_earnings}\n\n"
            f"*Earn now 👉* @notcoin\\_bot\n\n"
            f"Creator's blog: [EN](https://t.me/digital_man_blog) | [RU](https://t.me/digital_man)\n\n"
            f"[Subscribe to Notcoin Pools](https://t.me/coinpools)"
        )

        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown',
                               disable_web_page_preview=True)

    except Exception as e:
        await send_error_to_admin(str(e))

# Don't forget to close the bot session when done
async def close_bot():
    await bot.session.close()
