from discord.ext import commands

from core.bot import Bot


class OnReady(commands.Cog):

    def __init__(self, bot: Bot):

        self.bot: Bot = bot

    @commands.Cog.listener("on_ready")
    async def on_ready(self):

        print("Logged as " + self.bot.user.name + ", Ready")


def setup(bot: Bot):

    bot.add_cog(OnReady(bot))
