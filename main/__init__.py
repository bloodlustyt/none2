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
BOT_TOKEN = "5851808236:AAEc8zGr6Rd1EKbN5x3kAXXICMQepT24mJY"
FORCESUB = 1485129059
ACCESS = 630269331
MONGODB_URI = "mongodb+srv://psychopomp:Cracker@1000@psychopomp.fgbjrip.mongodb.net/?retryWrites=true&w=majority"
AUTH_USERS = 1058482162

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN) 
