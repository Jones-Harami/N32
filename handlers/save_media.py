# (c) @AbirHasan2005

import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.errors import FloodWait
from handlers.helpers import get_short_link, str_to_b64
from handlers.users_api import get_user

def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

async def forward_to_channel(bot: Client, message: Message, editable: Message):
    try:
        __SENT = await message.copy(Config.DB_CHANNEL)
        return __SENT
    except FloodWait as sl:
        if sl.value > 45:
            await asyncio.sleep(sl.value)
            await bot.send_message(
                chat_id=int(Config.LOG_CHANNEL),
                text=f"#FloodWait:\nGot FloodWait of `{str(sl.value)}s` from `{str(editable.chat.id)}` !!",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Ban User", callback_data=f"ban_user_{str(editable.chat.id)}")]
                    ]
                )
            )
        return await forward_to_channel(bot, message, editable)


async def save_batch_media_in_channel(bot: Client, editable: Message, message_ids: list, cmd):
    try:
        message_ids_str = ""
        for message in (await bot.get_messages(chat_id=editable.chat.id, message_ids=message_ids)):
            sent_message = await forward_to_channel(bot, message, editable)
            if sent_message is None:
                continue
            message_ids_str += f"{str(sent_message.id)} "
            await asyncio.sleep(2)
        SaveMessage = await bot.send_message(
            chat_id=Config.DB_CHANNEL,
            text=message_ids_str,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Delete Batch", callback_data="closeMessage")
            ]])
        )
        user_id = cmd.from_user.id
        user = await get_user(user_id)
        main_url = f"https://t.me/{Config.BOT_USERNAME}?start=Jokersbots_{str_to_b64(str(SaveMessage.id))}"
        short_url = await get_short_link(user, main_url)

        b_success_for_short = Config.SHORTNING_SUCCESS.format(main_url=user["main_url"], short_url=user["short_url"])
        button_main_url = InlineKeyboardButton("✌🏻ᴏʀɪɢɪɴᴀʟ ʟɪɴᴋ", callback_data=main_url)
        button_short_url = InlineKeyboardButton("🤏🏻sʜᴏʀᴛ ʟɪɴᴋ", callback_data=short_url)
        reply_markup = InlineKeyboardMarkup().add(button_main_url).add(button_short_url)
        await editable.edit(b_success_for_short, reply_markup=reply_markup)
        
        await bot.send_message(
            chat_id=int(Config.LOG_CHANNEL),
            text=f"#BATCH_SAVE:\n\n[{editable.reply_to_message.from_user.first_name}](tg://user?id={editable.reply_to_message.from_user.id}) Got Batch Link!",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Open Link", url=main_url)]])
        )
    except Exception as err:
        await editable.edit(f"Something Went Wrong!\n\n**Error:** `{err}`")
        await bot.send_message(
            chat_id=int(Config.LOG_CHANNEL),
            text=f"#ERROR_TRACEBACK:\nGot Error from `{str(editable.chat.id)}` !!\n\n**Traceback:** `{err}`",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Ban User", callback_data=f"ban_user_{str(editable.chat.id)}")]
                ]
            )
        )


async def save_media_in_channel(bot: Client, editable: Message, message: Message):
    try:
        forwarded_msg = await message.forward(Config.DB_CHANNEL)
        file_er_id = str(forwarded_msg.id)
        await forwarded_msg.reply_text(
            f"#PRIVATE_FILE:\n\n[{message.from_user.first_name}](tg://user?id={message.from_user.id}) Got File Link!",
            disable_web_page_preview=True)

        user_id = message.from_user.id
        user = await get_user(user_id)
        main_url = f"https://telegram.me/{Config.BOT_USERNAME}?start=Jokersbots_{str_to_b64(file_er_id)}"
        short_url = await get_short_link(user, main_url)

        s_success_for_short = Config.SHORTNING_SUCCESS.format(main_url=user["main_url"], short_url=user["short_url"])
        button_main_url = InlineKeyboardButton("✌🏻ᴏʀɪɢɪɴᴀʟ ʟɪɴᴋ", callback_data=main_url)
        button_short_url = InlineKeyboardButton("🤏🏻sʜᴏʀᴛ ʟɪɴᴋ", callback_data=short_url)
        reply_markup = InlineKeyboardMarkup().add(button_main_url).add(button_short_url)
        await editable.edit(s_success_for_short, reply_markup=reply_markup)


    except FloodWait as sl:
        if sl.value > 45:
            print(f"Sleep of {sl.value}s caused by FloodWait ...")
            await asyncio.sleep(sl.value)
            await bot.send_message(
                chat_id=int(Config.LOG_CHANNEL),
                text="#FloodWait:\n"
                     f"Got FloodWait of `{str(sl.value)}s` from `{str(editable.chat.id)}` !!",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Ban User", callback_data=f"ban_user_{str(editable.chat.id)}")]
                    ]
                )
            )
        await save_media_in_channel(bot, editable, message)
    except Exception as err:
        await editable.edit(f"Something Went Wrong!\n\n**Error:** `{err}`")
        await bot.send_message(
            chat_id=int(Config.LOG_CHANNEL),
            text="#ERROR_TRACEBACK:\n"
                 f"Got Error from `{str(editable.chat.id)}` !!\n\n"
                 f"**Traceback:** `{err}`",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Ban User", callback_data=f"ban_user_{str(editable.chat.id)}")]
                ]
            )
        )
