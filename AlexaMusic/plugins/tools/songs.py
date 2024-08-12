import os
import requests
import config
import aiohttp
import aiofiles

import yt_dlp
from yt_dlp import YoutubeDL
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from youtube_search import YoutubeSearch

from AlexaMusic import app
from AlexaMusic.plugins.play.filters import command

channel = "KHAYAL70"
def remove_if_exists(path):
    if os.path.exists(path):
        os.remove(path)
        
lnk= "https://t.me/" +config.SUPPORT_CHANNEL
@app.on_message(command(["song","/song", "بحث"]))
async def song_downloader(client, message: Message):
    query = " ".join(message.command[1:])
    m = await message.reply_text("<b>⇜ جـارِ البحث عـن المقطـع الصـوتـي . . .</b>")
ydl_ops = {
         format :  bestaudio[ext=m4a] ,
         keepvideo : True,
         prefer_ffmpeg : False,
         geo_bypass : True,
         outtmpl :  %(title)s.%(ext)s ,
         quite : True,
         proxy :  180.31.234.71:8080 
    }
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0][ url_suffix ]}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        await m.edit("- لم يتم العثـور على نتائج ؟!\n- حـاول مجـدداً . . .")
        print(str(e))
        return
    await m.edit("<b>⇜ جـارِ التحميل ▬▭ . . .</b>")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"ᴍʏ ᴡᴏʀʟᴅ 𓏺 @{channel} "
        host = str(info_dict["uploader"])
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        await m.edit("<b>⇜ جـارِ التحميل ▬▬ . . .</b>")
        
        await message.reply_audio(
            audio=audio_file,
            caption=rep,
            title=title,
            performer=host,
            thumb=thumb_name,
            duration=dur,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="𝐒𝐨𝐮𝐫𝐜𝐞 𝐋𝐨𝐋🧚‍♀", url=config.SUPPORT_CHANNEL),
                ],

            ]

        ),
        )
        await m.delete()

    except Exception as e:
        await m.edit(" error, wait for bot owner to fix")
        print(e)

    try:
        remove_if_exists(audio_file)
        remove_if_exists(thumb_name)
    except Exception as e:
        print(e)


@app.on_message(command(["فيديو", "video","تحميل فيديو"]))
async def video_search(client, message):
    ydl_opts = {
        "format": "best",
        "keepvideo": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quite": True,
    }
    query = " ".join(message.command[1:])
    try:
