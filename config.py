from dotenv import load_dotenv
import os

load_dotenv()

URL_SILVER = os.getenv("URL_SILVER")
CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")
DB_FILE = os.getenv("DB_FILE")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
