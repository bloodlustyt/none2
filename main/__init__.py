#ChauhanMahesh/Vasusen/DroneBots/COL

from telethon import TelegramClient
from decouple import config
import logging
import time

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# variables
API_ID = 3599592
API_HASH = "80865dfca1e192f81931cbf61203cfe7"
BOT_TOKEN = "5147519086:AAE4BKvnVw5fta_zqwDI7BhdkQv-7nmuWm4"
FORCESUB = 1720432898
ACCESS = int("100890533755")
MONGODB_URI = "mongodb+srv://Vasusen:darkmaahi@cluster0.o7uqb.mongodb.net/cluster0?retryWrites=true&w=majority"
AUTH_USERS = int("5351121397")

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN) 
