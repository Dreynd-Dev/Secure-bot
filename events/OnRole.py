import discord
from discord.ext import commands

from core.bot import Bot
from modules.AntiNuke import AntiNuke


class OnRole(commands.Cog):

    def __init__(self, bot: Bot):

        self.bot = bot

    @commands.Cog.listener("on_guild_role_create")
    async def on_guild_role_create(self, role: discord.Role):

        antiNuke: AntiNuke = self.bot.getInstance(role.guild.id, AntiNuke)

        if antiNuke.enabled:

            async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):

                if isinstance(entry.user, discord.Member):

                    await antiNuke.new_element(entry.user)

    @commands.Cog.listener("on_guild_role_update")
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):

        antiNuke: AntiNuke = self.bot.getInstance(after.guild.id, AntiNuke)

        if antiNuke.enabled:

            async for entry in after.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_update):

                if isinstance(entry.user, discord.Member):

                    await antiNuke.new_element(entry.user)

    @commands.Cog.listener("on_guild_role_delete")
    async def on_guild_role_delete(self, role: discord.Role):

        antiNuke: AntiNuke = self.bot.getInstance(role.guild.id, AntiNuke)

        if antiNuke.enabled:

            async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):

                if isinstance(entry.user, discord.Member):

                    await antiNuke.new_element(entry.user)


def setup(bot: Bot):

    bot.add_cog(OnRole(bot))
