import discord
from discord.ext import commands

from core.bot import Bot
from modules.AntiNuke import AntiNuke


class OnChannel(commands.Cog):

    def __init__(self, bot: Bot):

        self.bot = bot

    @commands.Cog.listener("on_guild_channel_create")
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):

        antiNuke: AntiNuke = self.bot.getInstance(channel.guild.id, AntiNuke)

        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):

            if isinstance(entry.user, discord.Member):

                await antiNuke.new_element(entry.user)

    @commands.Cog.listener("on_guild_channel_update")
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):

        antiNuke: AntiNuke = self.bot.getInstance(after.id, AntiNuke)

        async for entry in after.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):

            if isinstance(entry.user, discord.Member):

                await antiNuke.new_element(entry.user)

    @commands.Cog.listener("on_guild_channel_delete")
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):

        antiNuke: AntiNuke = self.bot.getInstance(channel.guild.id, AntiNuke)

        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):

            if isinstance(entry.user, discord.Member):

                await antiNuke.new_element(entry.user)


def setup(bot: Bot):

    bot.add_cog(OnChannel(bot))
