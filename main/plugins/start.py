#Github.com/Vasusen-code

import os
from .. import bot, ACCESS
from telethon import events, Button, TelegramClient

from pyrogram import idle
from main.plugins.main import Bot
from main.plugins.helpers import login, logout, start_bot
st = "__Send me Link of any message to clone it here, For private channel message, send invite link first.__\n\nSUPPORT: @TeamDrone\nDEV: @MaheshChauhan"

@bot.on(events.NewMessage(incoming=True, pattern="/start"))
async def start(event):
    await event.reply(f'{st}', 
                      buttons=[
                              [Button.inline("SET THUMB", data="sett"),
                               Button.inline("REM THUMB", data="remt")],
                              [Button.inline("START BOT", data="startbot"),
                               Button.inline("STOP BOT", data="stopbot")],
                              [Button.inline("LOG-IN", data="login"),
                               Button.inline("LOG-OUT", data="logout")],
                              ])
    tag = f'[{event.sender.first_name}](tg://user?id={event.sender_id})'
    await event.client.send_message(int(ACCESS), f'{tag} started the BOT\nUserID: {event.sender_id}') 
    try:
        await Bot.start()
        await idle()
    except Exception as e:
        if 'Client is already connected' in str(e):
            pass
        else:
            return
    
@bot.on(events.callbackquery.CallbackQuery(data="sett"))
async def sett(event):    
    Drone = event.client                    
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    async with Drone.conversation(event.chat_id) as conv: 
        xx = await conv.send_message("Send me any image for thumbnail as a `reply` to this message.")
        x = await conv.get_reply()
        if not x.media:
            xx.edit("No media found.")
        mime = x.file.mime_type
        if not 'png' in mime:
            if not 'jpg' in mime:
                if not 'jpeg' in mime:
                    return await xx.edit("No image found.")
        await xx.delete()
        t = await event.client.send_message(event.chat_id, 'Trying.')
        path = await event.client.download_media(x.media)
        if os.path.exists(f'{event.sender_id}.jpg'):
            os.remove(f'{event.sender_id}.jpg')
        os.rename(path, f'./{event.sender_id}.jpg')
        await t.edit("Temporary thumbnail saved!")
        
@bot.on(events.callbackquery.CallbackQuery(data="remt"))
async def remt(event):  
    Drone = event.client            
    await event.edit('Trying.')
    try:
        os.remove(f'{event.sender_id}.jpg')
        await event.edit('Removed!')
    except Exception:
        await event.edit("No thumbnail saved.")                        
    
    
@bot.on(events.NewMessage(incoming=True,func=lambda e: e.is_private))
async def access(event):
    await event.forward_to(ACCESS)

@bot.on(events.callbackquery.CallbackQuery(data="login"))
async def lin(event):
    Drone = event.client
    button = await event.get_message()
    msg = await button.get_reply_message()  
    await event.delete()
    async with Drone.conversation(event.chat_id) as conv: 
        try:
            xx = await conv.send_message("send me your `api_id` as a reply to this.")
            x = await conv.get_reply()
            i = x.text
            await xx.delete()                    
            if not i:               
                return await xx.edit("No response found.")
        except Exception as e: 
            print(e)
            return await xx.edit("An error occured while waiting for the response.")
        try:
            xy = await conv.send_message("send me the your `api_hash` as a reply to this.")  
            y = await conv.get_reply()
            h = y.text
            await xy.delete()                    
            if not h:                
                return await xy.edit("No response found.")
        except Exception as e: 
            print(e)
            return await xy.edit("An error occured while waiting for the response.")
        try:
            xz = await conv.send_message("send me the your `api_hash` as a reply to this.")  
            z = await conv.get_reply()
            s = z.text
            await xz.delete()                    
            if not s:                
                return await xz.edit("No response found.")
        except Exception as e: 
            print(e)
            return await xz.edit("An error occured while waiting for the response.")
        await login(event.sender_id, i, h, s) 
        await Drone.send_message(event.chat_id, "Login credentials saved, now click on START BOT button.")
        
@bot.on(events.callbackquery.CallbackQuery(data="logout"))
async def out(event):
    await event.edit("Trying to logout.")
    await logout(event.sender_id)
    await event.edit('successfully Logged out.')
    
@bot.on(events.callbackquery.CallbackQuery(data="startbot"))
async def stb(event):
    await event.edit('Trying to start.')
    s, o = await start_bot(event.sender_id)
    if s == True:
        await event.edit('Started!')
    else:
        await event.edit(o)
                         
@bot.on(events.callbackquery.CallbackQuery(data="stopbot"))
async def spb(event):   
    s, o= await get_bot(event.sender_id)
    if s == True:
        await o.stop()
        await event.edit("Bot stopped.")
    else:
        await event.edit(o)
