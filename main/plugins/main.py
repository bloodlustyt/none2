# Github.com/Vasusen-code

from main.plugins.helpers import get_link, forcesub, forcesub_text, join, set_timer, check_timer, screenshot
from main.plugins.display_progress import progress_for_pyrogram
from main.Database.database import Database
from decouple import config

API_ID = config("API_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)
FORCESUB = config("FORCESUB", default=None) 
ACCESS = config("ACCESS", default=None, cast=int)

from pyrogram.errors import FloodWait, BadRequest
from pyrogram import Client, filters, idle
from ethon.pyfunc import video_metadata

import re, time, asyncio, logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

process=[]
timer=[]

Bot = Client(
    "Simple-Pyrogram-Bot",
    bot_token=BOT_TOKEN,
    api_id=int(API_ID),
    api_hash=API_HASH
)

async def get_msg(userbot, client, sender, msg_link):
    chat = ""
    msg_id = int(msg_link.split("/")[-1])
    if 't.me/c/' in msg_link:
        st, r = check_timer(sender, process, timer) 
        if st == False:
            return await client.send_message(sender, r) 
        chat = int('-100' + str(msg_link.split("/")[-2]))
        try:
            msg = await userbot.get_messages(chat, msg_id)
            edit = await client.send_message(sender, 'Trying to process.')
            file = await userbot.download_media(
                msg,
                progress=progress_for_pyrogram,
                progress_args=(
                    userbot,
                    "**DOWNOOADING:**\n",
                    edit,
                    time.time()
                )
            )
            await edit.edit('Trying to Upload.')
            caption = ""
            if msg.text is not None:
                caption = msg.text
            if str(file).split(".")[-1] == 'mp4':
                data = video_metadata(file)
                duration = data["duration"]
                thumb_path = await screenshot(file, duration/2, sender)
                await client.send_video(
                    chat_id=sender,
                    video=file,
                    caption=caption,
                    supports_streaming=True,
                    duration=duration,
                    thumb=thumb_path,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        client,
                        '**UPLOADING:**\n',
                        edit,
                        time.time()
                    )
                )
            else:
                await client.send_document(
                    sender,
                    file, 
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        client,
                        '**UPLOADING:**\n',
                        edit,
                        time.time()
                    )
                )
            await edit.delete()
            await set_timer(client, sender, process, timer) 
            await userbot.stop()
        except Exception as e:
            await client.send_message(sender, F'ERROR: {str(e)}')
            return 
    else:
        chat =  msg_link.split("/")[-2]
        await client.copy_message(int(sender), chat, msg_id)
    
@Bot.on_message(filters.private)
async def clone(bot, event):
    link = get_link(event.text)
    if not link:
        return
    xx = await forcesub(bot, event.chat.id)
    if xx is True:
        await event.reply_text(text=forcesub_text)
        return
    userbot = ""
    MONGODB_URI = config("MONGODB_URI", default=None)
    db = Database(MONGODB_URI, 'saverestricted')
    i, h, s = await db.get_credentials(event.chat.id)
    if i and h and s is not None:
        try:
            userbot = Client(
                session_name=s, 
                api_hash=h,
                api_id=int(i))
            await userbot.start()
        except ValueError:
            return await event.reply("INVALID API_ID: Logout and Login back with correct `API_ID`")
        except Exception as e:
            return await event.reply(f"Error: {str(e)}")
    else:
        return await event.reply("Your login credentials not found.")
    if 't.me/+' in link:
        xy = await join(userbot, link)
        await event.reply_text(text=xy)
        return 
    if 't.me' in link:
        try:
            await get_msg(userbot, bot, event.chat.id, link)
        except BadRequest:
            return await event.reply('Channel not joined. Send invite link!')
        except FloodWait:
            return await event.reply('Too many requests, try again later.')
        except ValueError:
            return await event.reply('Send Only message link or Private channel invites.')
        except Exception as e:
            return await event.reply(f'Error: `{str(e)}`')         
          
