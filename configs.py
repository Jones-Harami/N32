# # (c) @AbirHasan2005

import os

class Config(object):
	API_ID = int(os.environ.get("API_ID", "20036136"))
	API_HASH = os.environ.get("API_HASH", "4a16864f4b6f956f8bb6003b726133a7")
	BOT_TOKEN = os.environ.get("BOT_TOKEN", "6830396889:AAHK7DIChutznkO_HbKhOGMNAgQDrmY84g0")
	BOT_USERNAME = os.environ.get("BOT_USERNAME", "Dark_Matter_v4_RoBot")
	DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "-1002139098224"))
	BOT_OWNER = [int(owner) for owner in os.environ.get("BOT_OWNER", "6934250556").split()]
	DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb+srv://jonesdee2k:gdj132549s@cluster0.1qnajcm.mongodb.net/?retryWrites=true&w=majority")
	UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "-1002020360256")
	LOG_CHANNEL = os.environ.get("LOG_CHANNEL", "-1002004055044")
	BANNED_USERS = set(int(x) for x in os.environ.get("BANNED_USERS", "").split())
	FORWARD_AS_COPY = bool(os.environ.get("FORWARD_AS_COPY", True))
	BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", True))
	BANNED_CHAT_IDS = list(set(int(x) for x in os.environ.get("BANNED_CHAT_IDS", "").split()))
	OTHER_USERS_CAN_SAVE_FILE = bool(os.environ.get("OTHER_USERS_CAN_SAVE_FILE", False))
	ADMIN = [int(admin) for admin in os.environ.get("ADMIN", "6934250556").split()]
	ABOUT_BOT_TEXT = f"""
ᴛʜɪs ɪs ᴀ ғɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ ғᴏʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss ᴏɴʟʏ 💀 

╭────[ 🔅Fɪʟᴇ Sᴛᴏʀᴇ Bᴏᴛ🔅]────⍟
│
┽➢❇️ᴍʏ ɴᴀᴍᴇ ➺ [𝐋𝐢𝐧𝐤 𝐒𝐭𝐨𝐫𝐞 𝐁𝐨𝐭](https://t.me/{BOT_USERNAME})
│
┽➤⭕ ʟᴀɴɢᴜᴀɢᴇ ➺ [𝐏𝐲𝐭𝐡𝐨𝐧](https://www.python.org)
│
┽➤⭕ ʟɪʙʀᴀʀʏ ➺ [𝐏𝐲𝐫𝐨𝐠𝐫𝐚𝐦](https://docs.pyrogram.org)
│
┽➣♻️ᴍʏ ᴏᴡɴᴇʀ ➺ [𝐃𝐚𝐫𝐤 𝐌𝐚𝐭𝐭𝐞𝐫™](https://t.me/Dark_Matter_v4_RoBot)
│
╰──────[ 😎 ]───────────⍟
"""
	ABOUT_DEV_TEXT = f"""
👤 Tʜɪs ʙᴏᴛ ɪs ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ ➳ [𝐃𝐚𝐫𝐤 𝐌𝐚𝐭𝐭𝐞𝐫™](https://t.me/Dark_Matter_v4_RoBot)"""
	HOME_TEXT = """
╭──〔👋 Hᴇʟʟᴏ [{}](tg://user?id={})〕──➣
│
╰➣🥰 ɪ ᴀᴍ ᴀ sᴛᴀʙʟᴇ ғɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ
╭──╯
╰────⌬
╭────⌬
╰➣🤭 ʜᴏᴘᴇ ʏᴏᴜ ᴀʀᴇ ᴇɴᴊᴏʏɪɴɢ
╭──╯
╰────⌬
╭────⌬
╰➢🎎 ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : [𝐃𝐚𝐫𝐤 𝐌𝐚𝐭𝐭𝐞𝐫™](https://t.me/Dark_Matter_v4_RoBot)
╭──╯
╰─➣〔✨ ʜᴀᴠᴇ ᴀ ɴɪᴄᴇ ᴅᴀʏ ✨〕──❍
"""
	SHORTENER_API_MESSAGE = """
╭──〔♻️sʜᴏʀᴛɴᴇʀ ᴘʀᴏᴄᴇss ♻〕──➣
│
┽➢ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴀᴅᴅ/ᴜᴘᴅᴀᴛᴇ sʜᴏʀᴛɴᴇʀ👇🏻
│
┽➣<code>/shortener base_site apikey</code>
│
╰──〔🥰 ᴘʀᴏᴄᴇss ᴇɴᴅ 🥰〕──❍

╭──〔 sʜᴏʀᴛᴇɴᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ 〕─❍
╰──────👇🏻
╭──────⌬
╰🌐 𝑾𝒆𝒃𝒔𝒊𝒕𝒆 ➻ 

<code>{base_site}</code>

╭──────⌬
╰🔐 𝑨𝒑𝒊 ➻ 

<code>{shortener_api}</code>

╭──────⌬
╰──〔 ʜᴇʀᴇ ᴡᴇ ɢᴏ ᴀɢᴀɪɴ 🚀〕─➣
"""
