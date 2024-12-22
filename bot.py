import asyncio
import json
import re
import traceback

import aiogram
from aiogram.types import Message

from config import BOT_TOKEN

bot = aiogram.Bot(BOT_TOKEN)
dispatcher = aiogram.Dispatcher()

@dispatcher.message()
async def message_handler(message: Message):
    try:
        text = message.text
        if not text:
            return

        text_low = text.lower().strip()
        with open('data.json', 'r') as read_file:
            data_json = json.load(read_file)

        if message.from_user.id not in data_json['users']:
            data_json['users'].append(message.from_user.id)
            with open('data.json', 'w') as write_file:
                json.dump(data_json, write_file, ensure_ascii=False)

        rres1 = re.fullmatch(r'(ключевые ?слова ?\n)(.+)', text_low, re.DOTALL)
        if rres1:
            all_keywords = re.findall('[^,;\n]+', rres1.group(2))
            data_json['keywords'] = all_keywords or []
            with open('data.json', 'w') as write_file:
                json.dump(data_json, write_file, ensure_ascii=False)
            await bot.send_message(message.from_user.id, 'Ключевые слова записаны')
        rres2 = re.fullmatch(r'(анти ?слова ?\n)(.+)', text_low, re.DOTALL)
        if rres2:
            all_antiwords = re.findall('[^,;\n]+', rres2.group(2))
            data_json['antiwords'] = all_antiwords or []
            with open('data.json', 'w') as write_file:
                json.dump(data_json, write_file, ensure_ascii=False)
            await bot.send_message(message.from_user.id, 'Анти слова записаны')
    except:
        traceback.print_exc()
        return

async def bot_start():
    while True:
        try:
            print('BOT STARTED')
            await dispatcher.start_polling(bot, handle_signals=False)
        except KeyboardInterrupt:
            break
        except:
            await asyncio.sleep(50)
            continue