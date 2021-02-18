#    Copyright (c) 2021 Infinity BOTs <https://t.me/Infinity_BOTs>
 
#    This program is free software: you can redistribute it and/or modify  
#    it under the terms of the GNU General Public License as published by  
#    the Free Software Foundation, version 3.
# 
#    This program is distributed in the hope that it will be useful, but 
#    WITHOUT ANY WARRANTY; without even the implied warranty of 
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
#    General Public License for more details.

import os
import aiohttp
from pyrogram import filters, Client
from pytube import YouTube
from youtubesearchpython import VideosSearch
from sample_config import Config
from ut import get_arg

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InlineQuery, InputTextMessageContent


Jebot = Client(
   "Song Downloader",
   api_id=Config.APP_ID,
   api_hash=Config.API_HASH,
   bot_token=Config.TG_BOT_TOKEN,
)

def yt_search(song):
    videosSearch = VideosSearch(song, limit=1)
    result = videosSearch.result()
    if not result:
        return False
    else:
        video_id = result["result"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        return url


class AioHttp:
    @staticmethod
    async def get_json(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.json()

    @staticmethod
    async def get_text(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.text()

    @staticmethod
    async def get_raw(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.read()


@Jebot.on_message(filters.command("s"))
async def song(client, message):
    message.chat.id
    user_id = message.from_user["id"]
    args = get_arg(message) + " " + "song"
    if args.startswith(" "):
        await message.reply("<b>Enter a song name❗\n\nExample: `/s guleba`</b>")
        return ""
    status = await message.reply(
             text="<b>Downloading your song, Plz wait 🥺\n\nMade by @Infinity_BOTs 🇱🇰</b>",
             disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [[
                                    InlineKeyboardButton(
                                        "Developer", url="https://t.me/ImJanindu")
                                ]]
                        ),
               parse_mode="html",
        reply_to_message_id=message.message_id
      )
    video_link = yt_search(args)
    if not video_link:
        await status.edit("<b>Song not found 😑</b>")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("<b>Failed to download song 🤕</b>")
        LOGGER.error(ex)
        return ""
    os.rename(download, f"{str(user_id)}.mp3")
    await Jebot.send_chat_action(message.chat.id, "upload_audio")
    await Jebot.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(user_id)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        performer=str(yt.author),
        reply_to_message_id=message.message_id,
    )
    await status.delete()
    os.remove(f"{str(user_id)}.mp3")

@Jebot.on_message(filters.command("start"))
async def start(client, message):
   await Jebot.send_message(
           chat_id=message.chat.id,
           text="""<b>Hey There, I'm a Song Downloader Bot

Made by @ImJanindu 🇱🇰

Hit help button to find out more about how to use me</b>""",   
                        reply_markup=InlineKeyboardMarkup(
                            [[
                                    InlineKeyboardButton(
                                        "Help", callback_data="help"),
                                    InlineKeyboardButton(
                                        "Channel", url="https://t.me/Infinity_BOTs")
                                ]]
                        ),        
        disable_web_page_preview=True,        
        parse_mode="html",
        reply_to_message_id=message.message_id
    )


@Jebot.on_message(filters.command("help"))
async def help(client, message):
    await Jebot.send_message(
           chat_id=message.chat.id,
           text="""<b>Send `/s [song name]` to download song

~ @Infinity_BOTs

[Example](https://telegra.ph/file/cc041e5f780e7427bc17a.mp4)</b>""",
        reply_to_message_id=message.message_id
    )

@Jebot.on_callback_query()
async def button(Jebot, update):
      cb_data = update.data
      if "help" in cb_data:
        await update.message.delete()
        await help(Jebot, update.message)

print(
    """
Bot Started!

Join @Infinity_BOTs
"""
)

Jebot.run()
