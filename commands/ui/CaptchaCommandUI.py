import discord
from discord.ui import Button, Modal, InputText

from typing import Callable

from core.bot import Bot
from modules.Captcha import Captcha


class SetRoleModal(Modal):

    def __init__(self, bot: Bot, captchaEmbed: Callable):

        self.bot: Bot = bot
        self.captchaEmbed: Callable = captchaEmbed

        super().__init__(
            InputText(
                label="Paste your role ID here...",
                style=discord.InputTextStyle.short
            ),
            title="Set Role",
        )

    async def callback(self, interaction: discord.Interaction):

        try:

            ID = int(self.children[0].value)
            role = interaction.guild.get_role(ID)

            if role is None:

                return

            captcha = self.bot.getInstance(interaction.guild_id, Captcha)
            captcha.roleID = ID

            self.bot.file.data[str(interaction.guild_id)]["Captcha"]["roleID"] = ID
            await self.bot.file.synchronize_data()

            await interaction.response.edit_message(
                embed=self.captchaEmbed(captcha)
            )

        except ValueError:

            pass


class SetRoleButton(Button):

    def __init__(self, bot: Bot, captchaEmbed: Callable):

        self.bot: Bot = bot
        self.captchaEmbed: Callable = captchaEmbed

        super().__init__(
            label="Set Role",
            style=discord.ButtonStyle.blurple
        )

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.send_modal(SetRoleModal(self.bot, self.captchaEmbed))


class SetChannelModal(Modal):

    def __init__(self, bot: Bot, captchaEmbed: Callable):

        self.bot: Bot = bot
        self.captchaEmbed: Callable = captchaEmbed

        super().__init__(
            InputText(
                label="Paste your channel ID here...",
                style=discord.InputTextStyle.short
            ),
            title="Set Channel",
        )

    async def callback(self, interaction: discord.Interaction):

        try:

            ID = int(self.children[0].value)
            channel = interaction.guild.get_channel(ID)

            if channel is None:
                return

            captcha = self.bot.getInstance(interaction.guild_id, Captcha)
            captcha.channelID = ID

            self.bot.file.data[str(interaction.guild_id)]["Captcha"]["channelID"] = ID
            await self.bot.file.synchronize_data()

            await interaction.response.edit_message(
                embed=self.captchaEmbed(captcha)
            )

        except ValueError:

            pass


class SetChannelButton(Button):

    def __init__(self, bot: Bot, captchaEmbed: Callable):

        self.bot: Bot = bot
        self.captchaEmbed: Callable = captchaEmbed

        super().__init__(
            label="Set Channel",
            style=discord.ButtonStyle.blurple
        )

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.send_modal(SetChannelModal(self.bot, self.captchaEmbed))
