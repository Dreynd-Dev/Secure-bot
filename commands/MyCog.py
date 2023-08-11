import discord
from discord.ext import commands


class MyCog(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @discord.slash_command(name="say")
    async def say(self, ctx: discord.ApplicationContext, message: str):

        await ctx.respond(message)


def setup(bot):

    bot.add_cog(MyCog(bot))
