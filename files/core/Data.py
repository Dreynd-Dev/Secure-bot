import json

from aiofile import async_open
from asyncio import Semaphore
from collections import defaultdict

defaultConfig = {
    "Whitelist": [

    ],
    "AntiNuke": {
        "enabled": True,
        "maxElements": 3,
        "expirationTime": 5
    },
    "AntiRaid": {
        "enabled": True,
        "maxElements": 5,
        "expirationTime": 15
    },
    "AntiSpam": {
        "enabled": True,
        "maxElements": 5,
        "expirationTime":5
    },
    "Captcha": {
        "enabled": False,
        "channelID": None,
        "roleID": None,
        "captchaLength": 6,
        "kickTime": 120,
        "noise": 0.50
    }
}


class Data:

    def __init__(self):

        self.__data: defaultdict
        self.__semaphore = Semaphore(1)

    async def load(self) -> None:

        async with async_open("files/json/data.json", "r", encoding="utf8") as f:

            self.__data = defaultdict(lambda: defaultConfig, json.loads(await f.read()))

    def getGuildData(self, guildID: int) -> dict:

        return self.__data[str(guildID)]

    async def updateGuildData(self, guildID: int, newData: dict) -> None:

        async with self.__semaphore:

            self.__data[str(guildID)] = newData

            data: str = json.dumps(dict(self.__data), indent=4, ensure_ascii=False)

            async with async_open("files/json/data.json", "w", encoding="utf8") as f:

                await f.write(data)
