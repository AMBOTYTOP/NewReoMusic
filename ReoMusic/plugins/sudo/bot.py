import psutil
import time
from ReoMusic import app 
from pyrogram import Client
from pyrogram import filters 
from pyrogram.types import Message
from ReoMusic.core.userbot import assistants
from ReoMusic.utils import bot_sys_stats
from ReoMusic import app
from ReoMusic.misc import SUDOERS
from ReoMusic.utils.database import (
    get_active_chats,
    get_active_video_chats,
    remove_active_chat,
    remove_active_video_chat,
)

start_time = time.time()

def time_formatter(milliseconds):
    minutes, seconds = divmod(int(milliseconds / 1000), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    tmp = (((str(weeks) + "ᴡ:") if weeks else "") +
           ((str(days) + "ᴅ:") if days else "") +
           ((str(hours) + "ʜ:") if hours else "") +
           ((str(minutes) + "ᴍ:") if minutes else "") +
           ((str(seconds) + "s") if seconds else ""))
    if not tmp:
        return "0s"
    if tmp.endswith(":"):
        return tmp[:-1]
    return tmp


@app.on_message(filters.command("bot"))
async def activevc(_, message: Message):
    uptime = time_formatter((time.time() - start_time) * 1000)
    cpu = psutil.cpu_percent()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    ac_audio = str(len(await get_active_chats()))
    ac_video = str(len(await get_active_video_chats()))
    TEXT = f"Uᴘᴛɪᴍᴇ» {UP} CPU Lᴏᴀᴅ» {CPU} ᴠᴏɪᴄᴇ» {ac_audio}"
    await message.reply(TEXT)
