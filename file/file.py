import json
import aiofile

from collections import defaultdict

defaultConfig = {
    "whitelist": [],
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


class File:

    def __init__(self):

        self.data: defaultdict

    async def load(self) -> None:

        try:

            async with aiofile.async_open("file/files/data.json", "r", encoding="utf8") as f:

                self.data = defaultdict(
                    lambda: defaultConfig,
                    json.loads(await f.read())
                )

        except Exception:

            pass

    async def synchronize_data(self) -> None:

        try:

            newData: str = json.dumps(dict(self.data), indent=4, ensure_ascii=False)

            async with aiofile.async_open("file/files/data.json", "w", encoding="utf8") as f:

                await f.write(newData)

        except Exception:

            pass
