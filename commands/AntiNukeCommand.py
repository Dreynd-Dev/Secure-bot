import discord
from discord.ext import commands

from core.bot import Bot
from commands.ui.ModuleView import ModuleView
from commands.core.Context import Context
from commands.core.Checks import whitelistOnly
from modules.AntiNuke import AntiNuke
from util.EmbedUtils import EmbedUtils


def antiNukeEmbed(antiNuke: AntiNuke):

    em = EmbedUtils.basicEmbed(
        title="AntiNuke",
        description="> AntiNuke module prevents your server from nuking. When a malicious user try too performs too "
                    "many dangerous actions in a limited time, he get punished !"
    )
    em.add_field(
        name="Enabled:",
        value="<:check:1112014748310065202>" if antiNuke.enabled else "<:cross:1112014825447510109>"
    )

    return em


class AntiNukeCommand(commands.Cog):

    @whitelistOnly()
    @discord.guild_only()
    @discord.slash_command(name="anti-nuke")
    async def _anti_nuke(self, ctx: Context):

        await ctx.response.defer(ephemeral=True)

        antiNuke = ctx.bot.getInstance(ctx.guild_id, AntiNuke)

        await ctx.send_followup(
            embed=antiNukeEmbed(antiNuke),
            view=ModuleView(ctx.bot, antiNuke, antiNukeEmbed))


def setup(bot: Bot):

    bot.add_cog(AntiNukeCommand())
