import discord
import asyncio

from core.bot import Bot
from modules.core.Module import Module
from modules.captcha.CaptchaCode import CaptchaCode


class Captcha(Module):

    def __init__(self, bot: Bot, guildID: int):

        super().__init__(
            enabled=bot.file.data[str(guildID)]["Captcha"]["enabled"]
        )

        self.channelID: int = bot.file.data[str(guildID)]["Captcha"]["channelID"]
        self.roleID: int = bot.file.data[str(guildID)]["Captcha"]["roleID"]
        self.captchaLength: int = bot.file.data[str(guildID)]["Captcha"]["captchaLength"]
        self.kickTime: int = bot.file.data[str(guildID)]["Captcha"]["kickTime"]
        self.noise: float = bot.file.data[str(guildID)]["Captcha"]["noise"]

    async def send_captcha(self, member: discord.Member):

        channel: discord.TextChannel = member.guild.get_channel(self.channelID)
        role: discord.Role = member.guild.get_role(self.roleID)

        if None not in (channel, role):

            captcha = CaptchaCode(
                member=member,
                channel=channel,
                role=role,
                captchaLength=self.captchaLength,
                kickTime=self.kickTime,
                noise=self.noise
            )
            captcha.new_captcha()

            await asyncio.gather(
                captcha.send_captcha_message(),
                captcha.start_timeout()
            )
