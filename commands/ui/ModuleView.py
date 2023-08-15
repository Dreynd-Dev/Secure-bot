import discord

from discord.ui import View, Button, button
from typing import Callable

from core.Bot import Bot
from modules.core.Module import Module


class ModuleView(View):

    def __init__(self, bot: Bot, module: Module, moduleEmbed: Callable):

        self.bot: Bot = bot
        self.module: Module = module
        self.moduleEmbed: Callable = moduleEmbed

        super().__init__(
            timeout=300
        )

    @button(label="Toggle !", style=discord.ButtonStyle.blurple)
    async def _toggle(self, interaction: discord.Interaction, button: discord.Button):

        await interaction.response.defer()

        self.module.toggle()

        guildData: dict = interaction.client.data.getGuildData(interaction.guild_id)
        guildData[self.module.__class__.__name__]["enabled"] = self.module.enabled

        await interaction.client.data.updateGuildData(interaction.guild_id, guildData)

        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            embed=self.moduleEmbed(self.module)
        )
