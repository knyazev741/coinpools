from dotenv import load_dotenv
import os

load_dotenv()

URL = os.getenv("URL")
LEVEL = os.getenv("LEVEL")
CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")
DB_FILE = os.getenv("DB_FILE")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
ADMIN_ID = os.getenv("ADMIN_ID")
