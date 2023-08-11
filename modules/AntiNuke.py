import discord

from core.bot import Bot
from modules.core.PPUserModule import PPUserModule
from modules.settings.MultiValuesSetting import MultiValueSetting


class AntiNuke(PPUserModule):

    def __init__(self, bot: Bot, guildID: int):

        self.bot: Bot = bot

        self.options: dict[str, MultiValueSetting] = {
            "maxElements": MultiValueSetting(
                name="Max Elements",
                description="",
                value=bot.file.data[str(guildID)]["AntiNuke"]["maxElements"],
                values=[3, 5, 10, 15, 25, 50]
            ),
            "expirationTime": MultiValueSetting(
                name="Expiration Time",
                description="",
                value=bot.file.data[str(guildID)]["AntiNuke"]["expirationTime"],
                values=[3, 5, 10, 15, 30, 60, 120, 180, 300, 600]
            )
        }

        super().__init__(
            enabled=bot.file.data[str(guildID)]["AntiNuke"]["enabled"],
            maxElements=bot.file.data[str(guildID)]["AntiNuke"]["maxElements"],
            expirationTime=bot.file.data[str(guildID)]["AntiNuke"]["expirationTime"],
        )

    async def _punishment(self, member: discord.Member):

        try:

            if member.bot:

                await member.kick()

            else:

                await member.ban()

        except Exception:

            pass
