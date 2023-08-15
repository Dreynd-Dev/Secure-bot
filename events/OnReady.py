from discord.ext import commands

from core.Bot import Bot


class OnReady(commands.Cog):

    def __init__(self, bot: Bot):

        self.bot: Bot = bot

    @commands.Cog.listener("on_ready")
    async def on_ready(self):

        await self.bot.tree.sync()

        print("Logged as " + self.bot.user.name + ", Ready")


async def setup(bot: Bot):

    await bot.add_cog(OnReady(bot))
