import asyncio
from pyrogram import Client, filters
from .database.users_sql import set_info


@Client.on_message(filters.private & filters.incoming & filters.command("auth"))
async def _auth(bot, msg):
    await msg.reply("**Authorize only if you trust us** \n\n"
                    "1) For authorizing you need to provide instagram username and password for your account "
                    "when asked.\n"
                    "2) We would suggest you to make a new account for this purpose as instagram can ban your "
                    "account for downloading content. \n\n"
                    "**Note** : We are not responsible for account bans")
    confirmation = await bot.ask(msg.user.id,
                                 "Do you wish to proceed? \n\nSend '`yes`' or '`y`' for positive confirmation.\nSend "
                                 "'`no`' or '`n`' to cancel authorization.")
    if confirmation.lower() in ['no', 'n', 'cancel', '/cancel']:
        await confirmation.reply("Authorization Cancelled", quote=True)
        return
    username = await bot.ask("Please send your Instagram Username")
    password = await bot.ask("Please send your Instagram Password")
    await msg.reply("Checking if Login credentials are valid...")
    command = f"instaloader --no-metadata-json -l {username} -p {password}"
    proc = await asyncio.subprocess.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if "wrong password" in str(stderr).lower():
        await msg.reply('Log in failed. \nWrong Instagram Password.\n\nPlease try authorizing again with /auth.')
        return
    await set_info(msg.user.id, username, password)
    await msg.reply("Authorizing was successful. You can download private posts and stories now!")
