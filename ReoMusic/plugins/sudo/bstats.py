from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait
from ReoMusic import app as AM
from ReoMusic.misc import SUDOERS
from ReoMusic.utils.database import (
    get_active_chats,
    get_authuser_names,
    get_client,
    get_served_chats,
    get_served_users,
)
from ReoMusic.utils.decorators.language import language
from ReoMusic.utils.formatters import alpha_to_int
from config import adminlist
import asyncio
from pyrogram import *
from pyrogram.types import *
from config import MONGO_DB_URI, REO
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
import random
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid

mongo = MongoCli(MONGO_DB_URI)

db = mongo.chats
db = db.chatsdb
#User 
db = mongo.users
db = db.users

AM_PIC = [
    "https://graph.org/file/b29c2cf5e67b67a7c2df4.jpg",
    "https://graph.org/file/b29c2cf5e67b67a7c2df4.jpg",
    "https://graph.org/file/b29c2cf5e67b67a7c2df4.jpg",
    "https://graph.org/file/b29c2cf5e67b67a7c2df4.jpg"
]

#CHATGROUP

async def get_chats():
  chat_list = []
  async for chat in db.chats.find({"chat": {"$lt": 0}}):
    chat_list.append(chat['chat'])
  return chat_list

async def get_chat(chat):
  chats = await get_chats()
  if chat in chats:
    return True
  else:
    return False

async def add_chat(chat):
  chats = await get_chats()
  if chat in chats:
    return
  else:
    await db.chats.insert_one({"chat": chat})

async def del_chat(chat):
  chats = await get_chats()
  if not chat in chats:
    return
  else:
    await db.chats.delete_one({"chat": chat})

#USERS
async def get_users():
  user_list = []
  async for user in db.users.find({"user": {"$gt": 0}}):
    user_list.append(user['user'])
  return user_list


async def get_user(user):
  users = await get_users()
  if user in users:
    return True
  else:
    return False

async def add_user(user):
  users = await get_users()
  if user in users:
    return
  else:
    await db.users.insert_one({"user": user})


async def del_user(user):
  users = await get_users()
  if not user in users:
    return
  else:
    await db.users.delete_one({"user": user})
      
      #GCAST
async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=user_id)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception:
        return 500, f"{user_id} : {traceback.format_exc()}\n"

@AM.on_message(filters.command("gcast") & filters.user(REO))
async def broadcast(_, message):
    if not message.reply_to_message:
        await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ ɪᴛ.")
        return    
    exmsg = await message.reply_text("sᴛᴀʀᴛᴇᴅ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ!")
    all_chats = (await get_chats()) or {}
    all_users = (await get_users()) or {}
    done_chats = 0
    done_users = 0
    failed_chats = 0
    failed_users = 0
    for chat in all_chats:
        try:
            await send_msg(chat, message.reply_to_message)
            done_chats += 1
            await asyncio.sleep(0.1)
        except Exception:
            pass
            failed_chats += 1

    for user in all_users:
        try:
            await send_msg(user, message.reply_to_message)
            done_users += 1
            await asyncio.sleep(0.1)
        except Exception:
            pass
            failed_users += 1
    if failed_users == 0 and failed_chats == 0:
        await exmsg.edit_text(
            f"**sᴜᴄᴄᴇssғᴜʟʟʏ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ✅**\n\n**sᴇɴᴛ ᴍᴇssᴀɢᴇ ᴛᴏ** `{done_chats}` **ᴄʜᴀᴛs ᴀɴᴅ** `{done_users}` **ᴜsᴇʀs**",
        )
    else:
        await exmsg.edit_text(
            f"**sᴜᴄᴄᴇssғᴜʟʟʏ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ✅**\n\n**sᴇɴᴛ ᴍᴇssᴀɢᴇ ᴛᴏ** `{done_chats}` **ᴄʜᴀᴛs** `{done_users}` **ᴜsᴇʀs**\n\n**ɴᴏᴛᴇ:-** `ᴅᴜᴇ ᴛᴏ sᴏᴍᴇ ɪssᴜᴇ ᴄᴀɴ'ᴛ ᴀʙʟᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ` `{failed_users}` **ᴜsᴇʀs ᴀɴᴅ** `{failed_chats}` **ᴄʜᴀᴛs**",
        )



@AM.on_message(filters.command("announce") & filters.user(REO))
async def announced(_, message):
    if message.reply_to_message:
      to_send=message.reply_to_message.id
    if not message.reply_to_message:
      return await message.reply_text("Reply To Some Post To Broadcast")
    chats = await get_chats() or []
    users = await get_users() or []
    print(chats)
    print(users)
    failed = 0
    for chat in chats:
      try:
        await AM.forward_messages(chat_id=int(chat), from_chat_id=message.chat.id, message_ids=to_send)
        await asyncio.sleep(1)
      except Exception:
        failed += 1
    
    failed_user = 0
    for user in users:
      try:
        await AM.forward_messages(chat_id=int(user), from_chat_id=message.chat.id, message_ids=to_send)
        await asyncio.sleep(1)
      except Exception as e:
        failed_user += 1


    await message.reply_text("Bʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇ. {} ɢʀᴏᴜᴘs ғᴀɪʟᴇᴅ ᴛᴏ ʀᴇᴄᴇɪᴠᴇ ᴛʜᴇ ᴍᴇssᴀɢᴇ, ᴘʀᴏʙᴀʙʟʏ ᴅᴜᴇ ᴛᴏ ʙᴇɪɴɢ ᴋɪᴄᴋᴇᴅ. {} ᴜsᴇʀs ғᴀɪʟᴇᴅ ᴛᴏ ʀᴇᴄᴇɪᴠᴇ ᴛʜᴇ ᴍᴇssᴀɢᴇ, ᴘʀᴏʙᴀʙʟʏ ᴅᴜᴇ ᴛᴏ ʙᴇɪɴɢ ʙᴀɴɴᴇᴅ. .".format(failed, failed_user))

#DBSAVE

@AM.on_message(group=10)
async def chat_watcher_func(_, message):
    try:
        if message.from_user:
            us_in_db = await get_user(message.from_user.id)
            if not us_in_db:
                await add_user(message.from_user.id)

        chat_id = (message.chat.id if message.chat.id != message.from_user.id else None)

        if not chat_id:
            return

        in_db = await get_chat(chat_id)
        if not in_db:
            await add_chat(chat_id)
    except:
        pass


@AM.on_message(filters.command(["bstats"], [".", "!", "/"]))
async def stats(cli: Client, message: Message):
    users = len(await get_users())
    chats = len(await get_chats())
    await message.reply_photo(
        photo=random.choice(AM_PIC),
        caption=f"""**ᴛᴏᴛᴀʟ sᴛᴀᴛs ᴏғ** {(await cli.get_me()).mention} :

➻ ᴄʜᴀᴛs : {chats}
➻ ᴜsᴇʀs : {users}
"""
    )
