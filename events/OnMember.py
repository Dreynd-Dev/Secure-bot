from discord import Member
from discord.ext import commands

from core.Bot import Bot
from modules.Captcha import Captcha


class OnMember(commands.Cog):

    def __init__(self, bot: Bot):

        self.bot: Bot = bot

    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member: Member):

        if not member.bot:

            captcha: Captcha = self.bot.getModuleInstance(member.guild.id, Captcha)

            if captcha.enabled:

                await captcha.send_captcha(member)


async def setup(bot: Bot):

    await bot.add_cog(OnMember(bot))
