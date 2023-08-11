import discord
from discord.ext import commands

from core.bot import Bot
from commands.core.Context import Context


def isWhitelisted(bot: Bot, member: discord.Member):

    return member == member.guild.owner or member.id in bot.file.data.get(str(member.guild.id), {}).get("whitelist", [])


def whitelistOnly():

    async def predicate(ctx: Context) -> bool:

        return isWhitelisted(ctx.bot, ctx.user)

    return commands.check(predicate)
