import discord
import datetime

from core.bot import Bot
from modules.core.PPUserModule import PPUserModule


class AntiSpam(PPUserModule):

    def __init__(self, bot, guildID: int):

        self.bot: Bot = bot

        super().__init__(
            enabled=bot.file.data[str(guildID)]["AntiSpam"]["enabled"],
            maxElements=bot.file.data[str(guildID)]["AntiSpam"]["maxElements"],
            expirationTime=bot.file.data[str(guildID)]["AntiSpam"]["expirationTime"]
        )

    async def _punishment(self, member: discord.Member):

        hours = 72
        until = datetime.datetime.utcnow() + datetime.timedelta(hours=hours)

        await member.timeout(until=until)
