import discord
from discord.ext import commands

from core.bot import Bot
from modules.AntiSpam import AntiSpam


class OnMessage(commands.Cog):

    def __init__(self, bot: Bot):

        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):

        if (isinstance(message.author, discord.Member) and not message.author.bot
                and not message.author.guild_permissions.manage_messages):

            antiSpam: AntiSpam = self.bot.getInstance(message.guild.id, AntiSpam)

            if antiSpam.enabled:

                await antiSpam.new_element(message.author)


def setup(bot: Bot):

    bot.add_cog(OnMessage(bot))
