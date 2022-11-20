# Github.com/Vasusen-code

from main.plugins.helpers import get_link, forcesub, forcesub_text, join, set_timer, check_timer, screenshot
from main.plugins.display_progress import progress_for_pyrogram
from main.Database.database import Database
from decouple import config

from pyrogram.errors import FloodWait, BadRequest
from pyrogram import Client, filters, idle
from ethon.pyfunc import video_metadata

import os, re, time, asyncio, logging

from .. import API_ID, API_HASH, BOT_TOKEN, FORCESUB, ACCESS, MONGODB_URI

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

process=[]
timer=[]

Bot = Client(
    "save-restricted-bot",
    bot_token=BOT_TOKEN,
    api_id=int(API_ID),
    api_hash=API_HASH
)

errorC = """Error: Couldn't start client by Login credentials. Check these:

- is your API details entered right? 
- Did you send "Pyrogram" string session? 
- Do not send string in bold, italic or any other fonts."""

async def get_msg(userbot, client, sender, msg_link, edit):
    chat = ""
    msg_id = int(msg_link.split("/")[-1])
    if 't.me/c/' in msg_link:
        st, r = check_timer(sender, process, timer) 
        if st == False:
            return await edit.edit(r) 
        chat = int('-100' + str(msg_link.split("/")[-2]))
        try:
            msg = await userbot.get_messages(chat, msg_id)
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
            await os.remove(file)
            await set_timer(client, sender, process, timer) 
        except Exception as e:
            await edit.edit(F'ERROR: {str(e)}')
            return 
    else:
        chat =  msg_link.split("/")[-2]
        await client.copy_message(int(sender), chat, msg_id)
        await edit.delete()
        
@Bot.on_message(filters.private & filters.incoming)
async def clone(bot, event):
    link = get_link(event.text)
    if not link:
        return
    xx = await forcesub(bot, event.chat.id)
    if xx is True:
        await event.reply(forcesub_text)
        return
    edit = await Bot.send_message(event.chat.id, 'Trying to process.')
    
    if 't.me' in link and not 't.me/c/' in link and not 't.me/+' in link:
        try:
            await get_msg(bot, bot, event.chat.id, link, edit)
        except FloodWait:
            return await edit.edit('Too many requests, try again later.')
        except ValueError:
            return await edit.edit('Send Only message link or Private channel invites.')
        except Exception as e:
            return await edit.edit(f'Error: `{str(e)}`')         

    userbot = ""
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
            return await edit.edit("INVALID API_ID: Logout and Login back with correct `API_ID`")
        except Exception as e:
            print(e)
            return await edit.edit(errorC)
    else:
        return await edit.edit("Your login credentials not found.")
    if 't.me/+' in link:
        xy = await join(userbot, link)
        await edit.edit(xy)
        return 
    if 't.me' in link:
        try:
            await get_msg(userbot, bot, event.chat.id, link, edit)
        except BadRequest.CHANNEL_INVALID:
            return await edit.edit('Channel not joined! Send invite link or join manually.')
        except FloodWait:
            return await edit.edit('Too many requests, try again later.')
        except Exception as e:
            return await edit.edit(f'Error: `{str(e)}`')         
