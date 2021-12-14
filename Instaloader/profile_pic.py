import os
import shutil
import instaloader
from pyrogram import Client, filters
from instaloader.exceptions import QueryReturnedNotFoundException, ProfileNotExistsException


@Client.on_message(filters.private & filters.command(["profile_pic", "dp"]))
async def dp(_, msg):
    status = await msg.reply('Please Wait...', quote=True)
    if len(msg.command) == 1:
        await msg.reply("Please do not use empty command. Below is the right format to get a profile pic. "
                        "\n\n`/profile_pic instagram-username` \n\nExample : `/profile_pic taaarannn`")
        return
    elif len(msg.command) > 2:
        await msg.reply("Use 1 username at a time.")
        return
    text = msg.command[1]
    if text.startswith('@'):
        text = text[1:]
    try:
        instaloader.Instaloader().download_profile(text, profile_pic_only=True)
    except (QueryReturnedNotFoundException, ProfileNotExistsException):
        await status.delete()
        await msg.reply("No Such Instagram Account Exists.", quote=True)
        return
    files = os.listdir(text.lower())
    for file in files:
        if file.endswith(".jpg"):
            caption = f"Profile Picture of [@{text}](https://instagram.com/{text}) \n\nBy @StarkBots"
            await msg.reply_photo(f"{text}/{file}", caption=caption)
            await status.delete()
    shutil.rmtree(text)
