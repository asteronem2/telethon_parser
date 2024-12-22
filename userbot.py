import asyncio
import json
import re
import traceback

from aiogram.types import MessageEntity, InlineKeyboardMarkup, InlineKeyboardButton
from telethon import TelegramClient
from telethon.events import NewMessage
from telethon.types import Message, PeerChat, PeerChannel

from config import API_ID, API_HASH

app = TelegramClient(
    session='telethon_session',
    api_id=API_ID,
    api_hash=API_HASH,
    app_version='Telethon 1.38.1',
    device_model='CPython 3.13.0',
    system_version='Darwin 24.0.0',
    lang_code='ru',
    flood_sleep_threshold=10
)

def main_filter(message: Message):
    if not message.message:
        return
    peer_type = type(message.peer_id)
    if peer_type in (PeerChannel, PeerChat):
        return True
    else:
        return False

@app.on(NewMessage())
async def handle_message(event: NewMessage.Event):
    try:
        import bot
        message: Message = event.message
        if not main_filter(message):
            return
        print(message.message)
        if message.entities:
            print([f'{i.to_dict()=}' for i in message.entities])
        else:
            print('0 entities')

        peer_type = type(message.peer_id)
        if peer_type == PeerChannel:
            chat_id = message.peer_id.channel_id
        elif peer_type == PeerChat:
            chat_id = message.peer_id.chat_id
        else:
            return

        convert_to_normal_entity = {
            'MessageEntityBold': 'bold',
            'MessageEntityBlockquote': 'blockquote',
            'MessageEntityUrl': 'url'
        }

        link_text = f'https://t.me/c/{chat_id}/{message.id}'

        data_json: dict
        with open('data.json', 'r') as read_file:
            data_json = json.load(read_file)

        text_low = message.message.lower().strip()

        have_keyword = False
        for keyword in data_json['keywords']:
            if re.search(keyword.lower(), text_low):
                have_keyword = True
                break
        have_antiword = False
        for antiword in data_json['antiwords']:
            if re.search(antiword.lower(), text_low):
                have_antiword = True
                break
        if have_keyword and not have_antiword:
            for user in data_json['users']:
                try:
                    await bot.bot.send_message(
                        chat_id=user,
                        text=message.message,
                        entities=[MessageEntity(
                            type=convert_to_normal_entity[i.to_dict()["_"]],
                            offset=i.offset,
                            length=i.length,
                            url=i.to_dict().get('url')
                        ) for i in message.entities if i.to_dict()["_"] in convert_to_normal_entity.keys()] if message.entities else None,
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Открыть 🔍', url=link_text)]])
                    )
                except:
                    continue
    except:
        traceback.print_exc()
        return
async def userbot_start():
    while True:
        try:
            print('USERBOT STARTED')
            await app.start()
            await app.run_until_disconnected()
        except KeyboardInterrupt:
            break
        except:
            await asyncio.sleep(50)
            continue