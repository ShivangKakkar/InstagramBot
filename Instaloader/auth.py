import asyncio
from pyrogram import Client, filters
from .database.users_sql import set_info, delete_info


@Client.on_message(filters.private & filters.incoming & filters.command("auth"))
async def _auth(bot, msg):
    await msg.reply("**Authorize only if you trust us** \n\n"
                    "1) For authorizing you need to provide instagram username and password for your account "
                    "when asked.\n"
                    "2) We would suggest you to make a new account for this purpose as instagram can ban your "
                    "account for downloading content. \n\n"
                    "**Note** : We are not responsible for account bans")
    confirmation = await bot.ask(msg.from_user.id,
                                 "**Do you wish to proceed?** \n\nSend '`yes`' or '`y`' for positive "
                                 "confirmation.\nSend '`no`' or '`n`' to cancel authorization.")
    if not confirmation.text.lower() in ['yes', 'y']:
        await confirmation.reply("Authorization Cancelled", quote=True)
        await msg.stop_propagation()
        return
    username = await bot.ask(msg.from_user.id, "Please send your Instagram Username", filters=filters.user(msg.from_user.id))
    password = await bot.ask(msg.from_user.id, "Please send your Instagram Password", filters=filters.user(msg.from_user.id))
    await msg.reply("Checking if login credentials are valid...")
    command = f"instaloader -l {username.text} -p {password.text}"
    proc = await asyncio.subprocess.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if "login error" in str(stderr).lower():
        await msg.reply(f'Log in failed. \n\n{str(stderr.decode("utf-8")).replace("Fatal error: Login error: ", "")} '
                        f'\nPlease try authorizing again with /auth.')
        return
    await set_info(msg.from_user.id, username.text, password.text)
    await msg.reply("Authorization was successful. You can download private posts now!")


@Client.on_message(filters.private & filters.incoming & filters.command("unauth"))
async def _unauth(_, msg):
    success = await delete_info(msg.from_user.id)
    if success:
        await msg.reply("Your credentials have been deleted from my database. \n\n"
                        "Now I can't access your account and you can't download private posts")
    else:
        await msg.reply("You didn't authorize me anyway!")
