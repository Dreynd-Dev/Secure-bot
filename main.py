import asyncio

from core.Bot import Bot


if __name__ == "__main__":

    bot = Bot()
    asyncio.run(bot.build())
