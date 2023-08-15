import asyncio

import discord

from modules.core.Module import Module
from modules.captcha.CaptchaCode import CaptchaCode


class Captcha(Module):

    def __init__(self):

        super().__init__(
            enabled=True
        )

    async def send_captcha(self, member: discord.Member):

        channel: discord.TextChannel = member.guild.get_channel(1139562691120353351)
        role: discord.Role = member.guild.get_role(1139562834154487830)

        if None not in (channel, role):

            codeCaptcha: CaptchaCode = CaptchaCode(member, channel, role,
                                                   6, 120, 0.50)

            codeCaptcha.newCaptcha()

            await asyncio.gather(
                codeCaptcha.sendCaptchaMessage(),
                codeCaptcha.startTimeout()
            )
