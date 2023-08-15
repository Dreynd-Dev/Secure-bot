from discord import app_commands, Embed, Interaction
from discord.ext import commands

from core.Bot import Bot
from util.EmbedUtils import EmbedUtils
from commands.ui.ModuleView import ModuleView
from commands.core.Checks import isWhitelist
from modules.AntiNuke import AntiNuke


class AntiNukeCommand(commands.Cog):

    def __init__(self, bot: Bot):

        self.bot: Bot = bot

    def antiNukeEmbed(self, antiNuke: AntiNuke) -> Embed:

        em: Embed = EmbedUtils.basicEmbed(
            title="AntiNuke",
            description="> AntiNuke module prevents your server from nuking. When a malicious user try too performs too "
                        "many dangerous actions in a limited time, he get punished !"
        )
        em.add_field(
            name="Enabled:",
            value="<:check:1112014748310065202>" if antiNuke.enabled else "<:cross:1112014825447510109>"
        )

        return em

    @app_commands.guild_only()
    @app_commands.check(isWhitelist)
    @app_commands.command(name="anti-nuke", description="Manage the anti nuke module.")
    async def _antiNuke(self, interaction: Interaction):

        await interaction.response.defer(ephemeral=True)

        antiNuke: AntiNuke = self.bot.getModuleInstance(interaction.guild_id, AntiNuke)

        await interaction.followup.send(
            embed=self.antiNukeEmbed(antiNuke),
            view=ModuleView(self.bot, antiNuke, self.antiNukeEmbed)
        )


async def setup(bot: Bot):

    await bot.add_cog(AntiNukeCommand(bot))
