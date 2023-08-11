import discord
from discord.ui import View, Button
from typing import Callable

from core.bot import Bot
from modules.core.Module import Module
from commands.core.Checks import isWhitelisted


class ToggleButton(Button):

    def __init__(self, bot: Bot, module: Module, moduleEmbed: Callable):

        self.bot: Bot = bot
        self.module: Module = module
        self.moduleEmbed: Callable = moduleEmbed

        super().__init__(
            label="Toggle",
            style=discord.ButtonStyle.blurple
        )

    async def callback(self, interaction: discord.Interaction):

        self.module.toggle()

        self.bot.file.data[str(interaction.guild_id)][self.module.__class__.__name__]["enabled"] = self.module.enabled
        await self.bot.file.synchronize_data()

        await interaction.response.edit_message(
            embed=self.moduleEmbed(self.module)
        )


class ModuleView(View):

    def __init__(self, bot: Bot, module: Module, moduleEmbed: Callable):

        self.bot: Bot = bot
        self.module: Module = module

        super().__init__(
            ToggleButton(bot, module, moduleEmbed),
            timeout=300,
            disable_on_timeout=True
        )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:

        return isWhitelisted(self.bot, interaction.user)

    async def on_check_failure(self, interaction: discord.Interaction) -> None:

        pass
