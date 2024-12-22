import asyncio

import userbot
import bot

async def main():
    await asyncio.gather(
        bot.bot_start(),
        userbot.userbot_start()
    )

if __name__ == '__main__':
    asyncio.run(main())
