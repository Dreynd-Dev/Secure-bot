import discord
from discord.ext import commands

from core.bot import Bot
from modules.Captcha import Captcha
from modules.AntiNuke import AntiNuke


class OnMember(commands.Cog):

    def __init__(self, bot: Bot):

        self.bot = bot

    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member: discord.Member):

        if not member.bot:

            captcha: Captcha = self.bot.getInstance(member.guild.id, Captcha)
            await captcha.send_captcha(member)

    @commands.Cog.listener("on_member_remove")
    async def on_member_remove(self, member: discord.Member):

        antiNuke: AntiNuke = self.bot.getInstance(member.guild.id, AntiNuke)

        if antiNuke.enabled:

            async for entry in member.guild.audit_logs(limit=1):

                if entry.action in [discord.AuditLogAction.kick, discord.AuditLogAction.ban] and entry.user != self.bot.user:

                    if isinstance(entry.user, discord.Member):

                        await antiNuke.new_element(entry.user)

    @commands.Cog.listener("on_member_update")
    async def on_member_update(self, before: discord.Member, after: discord.Member):

        pass

    @commands.Cog.listener("on_member_unban")
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):

        antiNuke: AntiNuke = self.bot.getInstance(guild.id, AntiNuke)

        if antiNuke.enabled:

            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.unban):

                if isinstance(entry.user, discord.Member):

                    await antiNuke.new_element(entry.user)


def setup(bot: Bot):

    bot.add_cog(OnMember(bot))
