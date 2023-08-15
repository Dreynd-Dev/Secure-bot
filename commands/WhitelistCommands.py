import discord

from discord import app_commands
from discord.ext import commands

from core.Bot import Bot
from util.EmbedUtils import EmbedUtils
from commands.core.Checks import isGuildOwner, isWhitelist


class WhitelistCommands(commands.GroupCog, name="whitelist"):

    def __init__(self, bot: Bot):

        self.bot: Bot = bot

    @app_commands.guild_only()
    @app_commands.check(isGuildOwner)
    @app_commands.command(name="add", description="Add a user to the whitelist.")
    async def _wl_add(self, interaction: discord.Interaction, member: discord.Member):

        await interaction.response.defer(ephemeral=True)

        guildData: dict = self.bot.data.getGuildData(interaction.guild_id)

        if member.id not in guildData["Whitelist"]:

            guildData["Whitelist"].append(member.id)
            await self.bot.data.updateGuildData(interaction.guild_id, guildData)

            em: discord.Embed = EmbedUtils.basicEmbed(
                title="Success !",
                description=member.mention + " has been successfully added to the whitelist !"
            )

            await interaction.followup.send(embed=em, ephemeral=True)

        else:

            em: discord.Embed = EmbedUtils.basicEmbed(
                title="Error !",
                description=member.mention + " is already in the whitelist !"
            )

            await interaction.followup.send(embed=em)

    @app_commands.guild_only()
    @app_commands.check(isGuildOwner)
    @app_commands.command(name="remove", description="Remove a user from the whitelist.")
    async def _wl_rm(self, interaction: discord.Interaction, member: discord.Member):

        await interaction.response.defer(ephemeral=True)

        guildData: dict = self.bot.data.getGuildData(interaction.guild_id)

        if member.id in guildData["Whitelist"]:

            guildData["Whitelist"].remove(member.id)
            await self.bot.data.updateGuildData(interaction.guild_id, guildData)

            em: discord.Embed = EmbedUtils.basicEmbed(
                title="Success !",
                description=member.mention + " has been successfully removed from the whitelist !"
            )

            await interaction.followup.send(embed=em, ephemeral=True)

        else:

            em: discord.Embed = EmbedUtils.basicEmbed(
                title="Error !",
                description=member.mention + " is not in the whitelist !"
            )

            await interaction.followup.send(embed=em)

    @app_commands.guild_only()
    @app_commands.check(isWhitelist)
    @app_commands.command(name="see", description="Display the current users in the whitelist !")
    async def _wl_see(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)

        guildData: dict = self.bot.data.getGuildData(interaction.guild_id)

        if guildData["Whitelist"]:

            formatted_ids: list[str] = [f"<@{userID}>" for userID in guildData["Whitelist"]]
            wl_members = ", ".join(formatted_ids)

        else:

            wl_members = "Actually, nobody is in the whitelist !"

        em = EmbedUtils.basicEmbed(
            title="Whitelist",
            description="> Whitelist is the list of members allowed to perform modifications to the bot parameters."
                        "Members in this list must be confidence member !\n"
                        "> **Note:** whitelisted members will be ignored by every protection systems !"
        )
        em.add_field(
            name="Members:",
            value=wl_members
        )

        await interaction.followup.send(embed=em)


async def setup(bot: Bot):

    await bot.add_cog(WhitelistCommands(bot))
