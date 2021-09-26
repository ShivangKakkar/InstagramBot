import os
import re
import shutil
from Config import INSTA_USERNAME, INSTA_PASSWORD
from pyrogram import Client, filters


@Client.on_message(filters.private & ~filters.command(["start", "help", "profile_pic", "about", "dp", "stats"]))
async def _instaloader(_, msg):
    pattern = re.compile(r'^(https?:[/][/])?(www\.)?instagram.com[/](p|reel)[/]([A-Za-z0-9-_]+)')
    try:
        matches = pattern.search(msg.text)
        post_id = matches.group(4)
        if INSTA_USERNAME and INSTA_PASSWORD:
            command = f"instaloader --no-metadata-json -l {INSTA_USERNAME} -p {INSTA_PASSWORD} -- -{post_id}"
        else:
            command = f"instaloader --no-metadata-json -- -{post_id}"
        os.system(command)
        path = f"-{post_id}"
        photos, videos, caption = post_prep(path)
        if not photos and not videos:
            await msg.reply("No Such Instagram Post Exists.")
            return
        if len(photos+videos) == 1:
            if photos:
                for photo in photos:
                    await msg.reply_photo(photo, caption)
            if videos:
                for video in videos:
                    await msg.reply_video(video, caption)
        else:
            if photos:
                for photo in photos:
                    await msg.reply_photo(photo)
            if videos:
                for video in videos:
                    await msg.reply_video(video)
            if caption:
                await msg.reply(f"**POST CAPTION : **\n\n{caption}")
        shutil.rmtree(path)
    except AttributeError:
        await msg.reply(error)


error = """
Please send me a valid instagram post link.
It must be like one of the given below

**Note** : To get profile picture of a account use "`/profile_pic instagram-username`". Link won't work.
"""


def post_prep(path):
    if not os.path.isdir(path):
        return None, None, None
    files = os.listdir(path)
    photos = []
    videos = []
    caption = ""
    for file in files:
        if file.endswith(".jpg"):
            photos.append(path+'/'+file)
        if file.endswith(".mp4"):
            videos.append(path+'/'+file)
        if file.endswith(".txt"):
            with open(f"{path}/{file}") as f:
                caption = f.read()
    return photos, videos, caption
