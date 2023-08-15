from discord import Message, Member
from discord.ext import commands

from core.Bot import Bot
from modules.AntiSpam import AntiSpam


class OnMessage(commands.Cog):

    def __init__(self, bot: Bot):

        self.bot: Bot = bot

    @commands.Cog.listener("on_message")
    async def on_message(self, message: Message):

        if not message.author.bot and not message.author.guild_permissions.manage_messages:

            antiSpam: AntiSpam = self.bot.getModuleInstance(message.guild.id, AntiSpam)

            if isinstance(message.author, Member):

                await antiSpam.new_element(message.author)


async def setup(bot: Bot):

    await bot.add_cog(OnMessage(bot))
