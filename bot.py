# (c) 

import os
import asyncio
import traceback
from binascii import (
    Error
)
from pyrogram import (
    Client,
    enums,
    filters
)
from pyrogram.errors import (
    UserNotParticipant,
    FloodWait,
    QueryIdInvalid
)
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message
)
from configs import Config
from handlers.database import db
from handlers.add_user_to_db import (
    add_user_to_database, 
    only_admin_access
) 
from handlers.send_file import send_media_and_reply
from handlers.helpers import b64_to_str, str_to_b64
from handlers.check_user_status import handle_user_status
from handlers.force_sub_handler import (
    handle_force_sub,
    get_invite_link
)
from handlers.broadcast_handlers import main_broadcast_handler
from handlers.save_media import (
    save_media_in_channel,
    save_batch_media_in_channel
)
from handlers.users_api import get_user, update_user_info

MediaList = {}

Bot = Client(
    name=Config.BOT_USERNAME,
    in_memory=True,
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)

@Bot.on_message(filters.private)
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)

@Bot.on_message(filters.command("start") & filters.private)
async def start(bot: Client, cmd: Message):

    if cmd.from_user.id in Config.BANNED_USERS:
        await cmd.reply_text("ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ 😔")
        return
    if Config.UPDATES_CHANNEL is not None:
        back = await handle_force_sub(bot, cmd)
        if back == 400:
            return

    usr_cmd = cmd.text.split("_", 1)[-1]
    if usr_cmd == "/start":
        await add_user_to_database(bot, cmd)
        await cmd.reply_text(
            Config.HOME_TEXT.format(cmd.from_user.first_name, cmd.from_user.id),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[
                InlineKeyboardButton("🗞️ ʙᴏᴛ ɪɴғᴏ", callback_data="aboutbot"),
                InlineKeyboardButton("«👤 ᴏᴡɴᴇʀ »", callback_data="aboutdevs")
                ],[
                InlineKeyboardButton("📑 ᴄʜᴀɴɴᴇʟ ʟɪsᴛ", url="https://t.me/all18_chennel"),
                InlineKeyboardButton("♀️ᴜᴘᴅᴀᴛᴇs ♂️", url="https://t.me/u0dates")
                ],[
                InlineKeyboardButton("✖sʟᴇᴇᴘ ᴍᴏᴅᴇ ✖", callback_data="closeMessage")
                ]]
            )
          )
    else:
        try:
            try:
                file_id = int(b64_to_str(usr_cmd).split("_")[-1])
            except (Error, UnicodeDecodeError):
                file_id = int(usr_cmd.split("_")[-1])
            GetMessage = await bot.get_messages(chat_id=Config.DB_CHANNEL, message_ids=file_id)
            message_ids = []
            if GetMessage.text:
                message_ids = GetMessage.text.split(" ")
                _response_msg = await cmd.reply_text(
                    text=f"**Total Files:** `{len(message_ids)}`",
                    quote=True,
                    disable_web_page_preview=True
                )
            else:
                message_ids.append(int(GetMessage.id))
            for i in range(len(message_ids)):
                await send_media_and_reply(bot, user_id=cmd.from_user.id, file_id=int(message_ids[i]))
        except Exception as err:
            await cmd.reply_text(f"sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ!\n\n**Error:** `{err}`")


@Bot.on_message((filters.document | filters.video | filters.audio | filters.photo) & ~filters.chat(Config.DB_CHANNEL))
async def main(bot: Client, message: Message):

    if message.chat.type == enums.ChatType.PRIVATE:
        user_id = message.from_user.id
        user = await get_user(user_id)

        await add_user_to_database(bot, message)

        if Config.UPDATES_CHANNEL is not None:
            back = await handle_force_sub(bot, message)
            if back == 400:
                return
        
        if message.from_user.id in Config.BANNED_USERS:
            await message.reply_text("ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ\n\n👉🏻 ᴄᴏɴᴛᴀᴄᴛ [𝐃𝐀𝐑𝐊 𝐌𝐀𝐓𝐓𝐄𝐑™](https://t.me/Horne2_EoBot)",
                                     disable_web_page_preview=True)
            return
            
        if user_id not in Config.ADMIN:
            await message.reply_text("⚠️ʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴛʜᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴛʜɪs ᴀᴄᴛɪᴏɴ")
            return

        await message.reply_text(
            text="**« 𝐂𝐡𝐨𝐨𝐬𝐞 𝐚𝐧 𝐎𝐩𝐭𝐢𝐨𝐧 𝐭𝐨 𝐔𝐩𝐥𝐨𝐚𝐝 𝐘𝐨𝐮𝐫 𝐅𝐢𝐥𝐞𝐬 »**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🅾️ʙᴀᴛᴄʜ ʟɪɴᴋ", callback_data="addToBatchTrue")],
                [InlineKeyboardButton("💯 ᴏɴʟʏ ʟɪɴᴋ", callback_data="addToBatchFalse")]
            ]),
            quote=True,
            disable_web_page_preview=True
        )
    elif message.chat.type == enums.ChatType.CHANNEL:
        if (message.chat.id == int(Config.LOG_CHANNEL)) or (message.chat.id == int(Config.UPDATES_CHANNEL)) or message.forward_from_chat or message.forward_from:
            return
        elif int(message.chat.id) in Config.BANNED_CHAT_IDS:
            await bot.leave_chat(message.chat.id)
            return
        else:
            pass

        try:
            forwarded_msg = await message.forword(Config.DB_CHANNEL)
            file_er_id = str(forwarded_msg.id)
            share_link = f"https://t.me/{Config.BOT_USERNAME}?start=DarkMatter_{str_to_b64(file_er_id)}"
            CH_edit = await bot.edit_message_reply_markup(message.chat.id, message.id,
                                                          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                                                              "Get Sharable Link", url=share_link)]]))
            if message.chat.username:
                await forwarded_msg.reply_text(
                    f"#CHANNEL_BUTTON:\n\n[{message.chat.title}](https://t.me/{message.chat.username}/{CH_edit.id}) Channel's Broadcasted File's Button Added!")
            else:
                private_ch = str(message.chat.id)[4:]
                await forwarded_msg.reply_text(
                    f"#CHANNEL_BUTTON:\n\n[{message.chat.title}](https://t.me/c/{private_ch}/{CH_edit.id}) Channel's Broadcasted File's Button Added!")
        except FloodWait as sl:
            await asyncio.sleep(sl.value)
            await bot.send_message(
                chat_id=int(Config.LOG_CHANNEL),
                text=f"#FloodWait:\nGot FloodWait of `{str(sl.value)}s` from `{str(message.chat.id)}` !!",
                disable_web_page_preview=True
            )
        except Exception as err:
            await bot.leave_chat(message.chat.id)
            await bot.send_message(
                chat_id=int(Config.LOG_CHANNEL),
                text=f"#ERROR_TRACEBACK:\nGot Error from `{str(message.chat.id)}` !!\n\n**Traceback:** `{err}`",
                disable_web_page_preview=True
            )
@Bot.on_message(filters.command('shortener') & filters.private)
async def shortener_api_handler(bot, m: Message):
    user_id = m.from_user.id
    user = await get_user(user_id)
    cmd = m.command

    if len(cmd) != 3:
        s = Config.SHORTENER_API_MESSAGE.format(base_site=user["base_site"], shortener_api=user["shortener_api"])
        return await m.reply(s)
        
    # extract base_site and shortener_api from the message
    base_site = m.command[1]
    shortener_api = m.command[2]

    await update_user_info(user_id, {"base_site": base_site, "shortener_api": shortener_api})
    await m.reply("ʏᴏᴜʀ sʜᴏʀᴛɴᴇʀ ᴡᴇʙsɪᴛᴇ ᴀɴᴅ ᴀᴘɪᴋᴇʏ ᴡᴀs ᴜᴘᴅᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ 🤩")

@Bot.on_message(filters.private & filters.command("broadcast") & filters.user(Config.BOT_OWNER) & filters.reply)
async def broadcast_handler_open(_, m: Message):
    await main_broadcast_handler(m, db)

@Bot.on_message(filters.private & filters.command("status") & filters.user(Config.BOT_OWNER))
async def sts(_, m: Message):
    total_users = await db.total_users_count()
    await m.reply_text(
        text=f"**Total Users in DB:** `{total_users}`",
        quote=True
    )

@Bot.on_message(filters.private & filters.command("ban_user") & filters.user(Config.BOT_OWNER))
async def ban(c: Client, m: Message):
    
    if len(m.command) == 1:
        await m.reply_text(
            f"ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ʙᴀɴ ᴀɴʏ ᴜsᴇʀ ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ\n\n"
            f"Usᴀɢᴇ ➠\n\n"
            f"`/ban_user user_id ban_duration ban_reason`\n\n"
            f"Eg: `/ban_user 1234567 28 You misused me.`\n"
            f"ᴛʜɪs ᴡɪʟʟ ʙᴀɴ ᴜsᴇʀ ᴡɪᴛʜ ɪᴅ `1234567` ғᴏʀ `28` ᴅᴀʏs ғᴏʀ ᴛʜᴇ ʀᴇᴀsᴏɴ `You misused me`.",
            quote=True
        )
        return

    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = ' '.join(m.command[3:])
        ban_log_text = f"Banning user {user_id} for {ban_duration} days for the reason {ban_reason}."
        try:
            await c.send_message(
                user_id,
                f"🛡️ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ ғᴏʀ **{ban_duration}** day(s) ғᴏʀ ᴛʜᴇ ʀᴇᴀsᴏɴ __{ban_reason}__ \n\n"
                f"**ᴍᴇssᴀɢᴇ ғʀᴏᴍ ᴀᴅᴍɪɴs**"
            )
            ban_log_text += '\n\nUser notified successfully!'
        except:
            traceback.print_exc()
            ban_log_text += f"\n\nUser notification failed! \n\n`{traceback.format_exc()}`"

        await db.ban_user(user_id, ban_duration, ban_reason)
        print(ban_log_text)
        await m.reply_text(
            ban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"Error occoured! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True
        )


@Bot.on_message(filters.private & filters.command("unban_user") & filters.user(Config.BOT_OWNER))
async def unban(c: Client, m: Message):

    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to unban any user.ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴜɴʙᴀɴ ᴀɴʏ ᴜsᴇʀ\n\n"
            f"Usᴀɢᴇ ➠\n\n`/unban_user user_id`\n\n"
            f"Eg: `/unban_user 1234567`\n"
            f"ᴛʜɪs ᴡɪʟʟ ᴜɴʙᴀɴ ᴜsᴇʀ ᴡɪᴛʜ ɪᴅ `1234567`.",
            quote=True
        )
        return

    try:
        user_id = int(m.command[1])
        unban_log_text = f"Unbanning user {user_id}"
        try:
            await c.send_message(
                user_id,
                f"🎉 ʏᴏᴜʀ ʙᴀɴ ᴡᴀs ʟɪғᴛᴇᴅ 🤩"
            )
            unban_log_text += '\n\nUser notified successfully!'
        except:
            traceback.print_exc()
            unban_log_text += f"\n\nUser notification failed! \n\n`{traceback.format_exc()}`"
        await db.remove_ban(user_id)
        print(unban_log_text)
        await m.reply_text(
            unban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"Error occurred! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True
        )


@Bot.on_message(filters.private & filters.command("banned_users") & filters.user(Config.BOT_OWNER))
async def _banned_users(_, m: Message):
    
    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ''

    async for banned_user in all_banned_users:
        user_id = banned_user['id']
        ban_duration = banned_user['ban_status']['ban_duration']
        banned_on = banned_user['ban_status']['banned_on']
        ban_reason = banned_user['ban_status']['ban_reason']
        banned_usr_count += 1
        text += f"> **user_id**: `{user_id}`, **Ban Duration**: `{ban_duration}`, " \
                f"**Banned on**: `{banned_on}`, **Reason**: `{ban_reason}`\n\n"
    reply_text = f"Total banned user(s): `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open('banned-users.txt', 'w') as f:
            f.write(reply_text)
        await m.reply_document('banned-users.txt', True)
        os.remove('banned-users.txt')
        return
    await m.reply_text(reply_text, True)


@Bot.on_message(filters.private & filters.command("clear_batch"))
async def clear_user_batch(bot: Client, m: Message):
    MediaList[f"{str(m.from_user.id)}"] = []
    await m.reply_text("Cleared your batch files successfully!")


@Bot.on_callback_query()
async def button(bot: Client, cmd: CallbackQuery):

    cb_data = cmd.data
    if "aboutbot" in cb_data:
        await cmd.message.edit(
            Config.ABOUT_BOT_TEXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[
                InlineKeyboardButton("🏦 ʜᴏᴍᴇ", callback_data="gotohome"),
                InlineKeyboardButton("«👤 ᴏᴡɴᴇʀ »", callback_data="aboutdevs")
                ]]
            )
        )

    elif "aboutdevs" in cb_data:
        await cmd.message.edit(
            Config.ABOUT_DEV_TEXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[
                InlineKeyboardButton("🗞️ ʙᴏᴛ ɪɴғᴏ", callback_data="aboutbot"),
                InlineKeyboardButton("🏦 ʜᴏᴍᴇ", callback_data="gotohome")
                ]]
            )
        )

    elif "gotohome" in cb_data:
        await cmd.message.edit(
            Config.HOME_TEXT.format(cmd.message.chat.first_name, cmd.message.chat.id),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[
                InlineKeyboardButton("🗞️ ʙᴏᴛ ɪɴғᴏ", callback_data="aboutbot"),
                InlineKeyboardButton("«👤 ᴏᴡɴᴇʀ »", callback_data="aboutdevs")
                ],[
                InlineKeyboardButton("📑 ᴄʜᴀɴɴᴇʟ ʟɪsᴛ", url="https://t.me/all18_chennel"),
                InlineKeyboardButton("♀️ᴜᴘᴅᴀᴛᴇs ♂️", url="https://t.me/u0dates")
                ],[
                InlineKeyboardButton("✖sʟᴇᴇᴘ ᴍᴏᴅᴇ ✖", callback_data="closeMessage")
                ]]
            )
        )

    elif "refreshForceSub" in cb_data:
        if Config.UPDATES_CHANNEL:
            if Config.UPDATES_CHANNEL.startswith("-100"):
                channel_chat_id = int(Config.UPDATES_CHANNEL)
            else:
                channel_chat_id = Config.UPDATES_CHANNEL
            try:
                user = await bot.get_chat_member(channel_chat_id, cmd.message.chat.id)
                if user.status == "kicked":
                    await cmd.message.edit(
                        text="ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ\n\n👉🏻 ᴄᴏɴᴛᴀᴄᴛ [𝐃𝐀𝐑𝐊 𝐌𝐀𝐓𝐓𝐄𝐑™](https://t.me/Horne2_EoBot)",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                invite_link = await get_invite_link(channel_chat_id)
                await cmd.message.edit(
                    text="sɪʀ,ɪ ʟɪᴋᴇ ʏᴏᴜʀ sᴍᴀʀᴛɴᴇss ʙᴜᴛ ᴅᴏɴ'ᴛ ʙᴇ ᴏᴠᴇʀsᴍᴀʀᴛ 🥴",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("⚕ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ⚕", url=invite_link.invite_link)
                            ],
                            [
                                InlineKeyboardButton("♻️ ʀᴇғʀᴇsʜ ♻", callback_data="refreshmeh")
                            ]
                        ]
                    )
                )
                return
            except Exception:
                await cmd.message.edit(
                    text="sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ\n\n👉🏻 ᴄᴏɴᴛᴀᴄᴛ [𝐃𝐀𝐑𝐊 𝐌𝐀𝐓𝐓𝐄𝐑™](https://t.me/Horne2_EoBot)",
                    disable_web_page_preview=True
                )
                return
        await cmd.message.edit(
            text=Config.HOME_TEXT.format(cmd.message.chat.first_name, cmd.message.chat.id),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[
                InlineKeyboardButton("🗞️ ʙᴏᴛ ɪɴғᴏ", callback_data="aboutbot"),
                InlineKeyboardButton("«👤 ᴏᴡɴᴇʀ »", callback_data="aboutdevs")
                ],[
                InlineKeyboardButton("📑 ᴄʜᴀɴɴᴇʟ ʟɪsᴛ", url="https://t.me/all18_chennel"),
                InlineKeyboardButton("♀️ᴜᴘᴅᴀᴛᴇs ♂️", url="https://t.me/u0dates")
                ],[
                InlineKeyboardButton("✖sʟᴇᴇᴘ ᴍᴏᴅᴇ ✖", callback_data="closeMessage")
                ]]
            )
        )

    elif cb_data.startswith("ban_user_"):
        user_id = cb_data.split("_", 2)[-1]
        if Config.UPDATES_CHANNEL is None:
            await cmd.answer("sᴏʀʀʏ sɪʀ, ʏᴏᴜ ᴅɪᴅɴ'ᴛ sᴇᴛ ᴀɴʏ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ!", show_alert=True)
            return
        if not int(cmd.from_user.id) == Config.BOT_OWNER:
            await cmd.answer("⚠️ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴅᴏ ᴛʜᴀᴛ 😡", show_alert=True)
            return
        try:
            await bot.kick_chat_member(chat_id=int(Config.UPDATES_CHANNEL), user_id=int(user_id))
            await cmd.answer("User Banned from Updates Channel!", show_alert=True)
        except Exception as e:
            await cmd.answer(f"Can't Ban Him!\n\nError: {e}", show_alert=True)

    elif "addToBatchTrue" in cb_data:
        if MediaList.get(f"{str(cmd.from_user.id)}", None) is None:
            MediaList[f"{str(cmd.from_user.id)}"] = []
        file_id = cmd.message.reply_to_message.id
        MediaList[f"{str(cmd.from_user.id)}"].append(file_id)
        await cmd.message.edit("ғɪʟᴇs sᴀᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ 🎉\n\n"
                               "ᴘʀᴇss ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ʙᴀᴛᴄʜ ʟɪɴᴋs",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("🔗 ɢᴇᴛ ʟɪɴᴋ", callback_data="getBatchLink")],
                                   [InlineKeyboardButton("ᴄʟᴏsᴇ 🚪", callback_data="closeMessage")]
                               ]))

    elif "addToBatchFalse" in cb_data:
        await save_media_in_channel(bot, editable=cmd.message, message=cmd.message.reply_to_message)

    elif "getBatchLink" in cb_data:
        message_ids = MediaList.get(f"{str(cmd.from_user.id)}", None)
        if message_ids is None:
            await cmd.answer("Batch List Empty!", show_alert=True)
            return
        await cmd.message.edit("Please wait....\n\n Your Files Downloding 📥")
        await cmd.message.edit(
            text="❄❅❅"
        )
        await asyncio.sleep(0.5)
        await cmd.message.edit(
            text="❄❄❅"
        )
        await asyncio.sleep(1)
        await cmd.message.edit(
            text="❄❄❄"
        )
        await save_batch_media_in_channel(bot=bot, editable=cmd.message, message_ids=message_ids, cmd=cmd)
        MediaList[f"{str(cmd.from_user.id)}"] = []

    elif "closeMessage" in cb_data:
        await cmd.message.delete(True)

    try:
        await cmd.answer()
    except QueryIdInvalid: pass


Bot.run()
