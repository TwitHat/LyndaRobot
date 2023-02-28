# Wallpapers module by @TheRealPhoenix using wall.alphacoders.com

import requests as r
from random import randint
from time import sleep

from telegram import Message, Chat, Update, Bot
from telegram.ext import run_async

from lynda import dispatcher, WALL_API
from lynda.modules.disable import DisableAbleCommandHandler


@run_async
def wall(bot: Bot, update: Update, args):
    msg = update.effective_message
    if query := " ".join(args):
        term = query.replace(" ", "%20")
        json_rep = r.get(f"https://wall.alphacoders.com/api2.0/get.php?auth={WALL_API}&method=search&term={term}").json()
        chat_id = update.effective_chat.id
        msg_id = update.effective_message.message_id
        if not json_rep.get("success"):
            msg.reply_text("An error occurred! Report this @Aman_Ahmed")
        elif wallpapers := json_rep.get("wallpapers"):
            index = randint(0, len(wallpapers)-1) # Choose random index
            wallpaper = wallpapers[index]
            wallpaper = wallpaper.get("url_image")
            wallpaper = wallpaper.replace("\\", "")
            caption = query
            bot.send_photo(chat_id, photo=wallpaper, caption='Preview',
            reply_to_message_id=msg_id, timeout=60)
            bot.send_document(chat_id, document=wallpaper,
            filename='wallpaper', caption=caption, reply_to_message_id=msg_id,
            timeout=60)
        else:
            msg.reply_text("No results found! Refine your search.")
            return
    else:
        msg.reply_text("Please enter a query!")
        return



__help__ = """
 - /wall <query>: get a a wallpaper from wall.alphacoders.com
"""

__mod_name__ = "Wallpaper"
WALL_HANDLER = DisableAbleCommandHandler("wall", wall, pass_args=True)
dispatcher.add_handler(WALL_HANDLER)