import re
from time import time

from pyrogram import filters
from pyrogram.types import ChatPermissions

from wbb import SUDOERS , DEVS, app
from wbb.core.decorators.errors import capture_err
from wbb.core.decorators.permissions import adminsOnly
from wbb.modules.admin import list_admins
from wbb.utils.dbfunctions import (
    delete_discmd,
    get_discmd,
    save_discmd,
)

__MODULE__ = "Blacklist"
__HELP__ = """
/disabled - Get All The Disabled Command In The Chat.
/disable [COMMAND] - Disable a command(only admin).
/enable [COMMAND] - Enable a command(only admin).
"""

@app.on_message(filters.command("enable") & ~filters.private)
@adminsOnly("can_change_info")
async def save_filters(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage:\n/enable command")
    word = message.text.split(None, 1)[1].strip()
    if not word:
        return await message.reply_text("**Usage**\n__/enable command__")
    chat_id = message.chat.id
    await delete_discmd(chat_id, word)
    await message.reply_text(f"__**Enabled {word}.**__")


@app.on_message(filters.command("disable") & ~filters.private)
@adminsOnly("can_change_info")
async def save_filters(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage:\n/__disable command__")
    word = message.text.split(None, 1)[1].strip()
    if not word:
        return await message.reply_text("**Usage**\n__/disable command__")
    chat_id = message.chat.id
    await save_discmd(chat_id, word)
    await message.reply_text(f"__**Enabled {word}.**__")

@app.on_message(filters.command("disabled") & ~filters.private)
@capture_err
async def get_filterss(_, message):
    data = await get_discmd(message.chat.id)
    if not data:
        await message.reply_text("**No disabled command in this chat.**")
    else:
        msg = f"List of disabled command in {message.chat.title} :\n"
        for word in data:
            msg += f"**-** `{word}`\n"
        await message.reply_text(msg)
