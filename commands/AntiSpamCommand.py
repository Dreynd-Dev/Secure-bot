import discord
from discord.ext import commands

from core.bot import Bot
from commands.ui.ModuleView import ModuleView
from commands.core.Context import Context
from commands.core.Checks import whitelistOnly
from modules.AntiSpam import AntiSpam
from util.EmbedUtils import EmbedUtils


def antiSpamEmbed(antiSpam: AntiSpam):

    em = EmbedUtils.basicEmbed(
        title="AntiSpam",
        description="> AntiSpam module prevents your server from spamming. When a malicious user try too send too "
                    "many messages in a limited time, he get punished !"
    )
    em.add_field(
        name="Enabled:",
        value="<:check:1112014748310065202>" if antiSpam.enabled else "<:cross:1112014825447510109>"
    )

    return em


class AntiSpamCommand(commands.Cog):

    @whitelistOnly()
    @discord.guild_only()
    @discord.slash_command(name="anti-spam")
    async def _anti_spam(self, ctx: Context):

        await ctx.response.defer(ephemeral=True)

        antiSpam = ctx.bot.getInstance(ctx.guild_id, AntiSpam)

        await ctx.send_followup(
            embed=antiSpamEmbed(antiSpam),
            view=ModuleView(ctx.bot, antiSpam, antiSpamEmbed))


def setup(bot: Bot):

    bot.add_cog(AntiSpamCommand())
