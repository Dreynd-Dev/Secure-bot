from discord import app_commands, Embed, Interaction
from discord.ext import commands

from core.Bot import Bot
from util.EmbedUtils import EmbedUtils
from commands.ui.ModuleView import ModuleView
from commands.core.Checks import isWhitelist
from modules.AntiSpam import AntiSpam


class AntiSpamCommand(commands.Cog):

    def __init__(self, bot: Bot):

        self.bot: Bot = bot

    def antiSpamEmbed(self, antiSpam: AntiSpam) -> Embed:

        em: Embed = EmbedUtils.basicEmbed(
            title="AntiSpam",
            description="> AntiSpam module prevents your server from spamming. When a malicious user try too send too "
                        "many messages in a limited time, he get punished !"
        )
        em.add_field(
            name="Enabled:",
            value="<:check:1112014748310065202>" if antiSpam.enabled else "<:cross:1112014825447510109>"
        )

        return em

    @app_commands.guild_only()
    @app_commands.check(isWhitelist)
    @app_commands.command(name="anti-spam", description="Manage the anti spam module.")
    async def _antiSpam(self, interaction: Interaction):

        await interaction.response.defer(ephemeral=True)

        antiSpam: AntiSpam = self.bot.getModuleInstance(interaction.guild_id, AntiSpam)

        await interaction.followup.send(
            embed=self.antiSpamEmbed(antiSpam),
            view=ModuleView(self.bot, antiSpam, self.antiSpamEmbed)
        )


async def setup(bot: Bot):

    await bot.add_cog(AntiSpamCommand(bot))
