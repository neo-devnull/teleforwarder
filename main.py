from telethon.sync import TelegramClient, events, errors
from os import path

import config as cfg
import functions 
import asyncio
import logging 
import json 
import os 


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
allowed_chats = list(cfg.chats.keys())
allowed_chats = [int(chat) for chat in allowed_chats]

if not os.path.exists('dl'):
    os.mkdir('dl')

with TelegramClient('name', cfg.api_id, cfg.api_hash) as client:

    @client.on(events.NewMessage(outgoing=True,chats=allowed_chats))
    async def handler(event):
        chat_id = str(event.message.chat_id)          
        chat_settings = cfg.chats.get(chat_id)

        #Some vars that we will use later 
        allowed_types = chat_settings.get('allow',['text','photo']) 
        text_filters = chat_settings.get('text_filters')       
        send_media = False 
        downloaded_file = None  
        
        #Validations
        #There's no media, check if text messages are in allowed types 
        if not event.message.media and not 'text' in allowed_types:
            return False    

        #Check if the message media is allowed 
        if event.message.media:
            media_type = functions.get_media_type(event.message)            
            if not media_type in allowed_types:
                return False

            send_media = True             

        #Check if the text is allowed 
        if text_filters:
            if not functions.allow_text(event.message.text,text_filters):
                return False 

        #Time to forward/send
        to = int(chat_settings['to'])

        if send_media:
            downloaded_file = await event.message.download_media(file='./dl/') 
        
        await client.send_message(
            entity = to,
            message = event.message.text,
            file = downloaded_file
        )  

        #Delete downloaded file 
        if downloaded_file:
            os.unlink(downloaded_file)


    client.run_until_disconnected()