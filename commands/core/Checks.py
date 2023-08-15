from discord import Interaction

from commands.core.Errors import *


async def isGuildOwner(interaction: Interaction) -> bool:

    if interaction.user == interaction.guild.owner:

        return True

    raise NotOwner


async def isWhitelist(interaction: Interaction) -> bool:

    guildData: dict = interaction.client.data.getGuildData(interaction.guild_id)

    if await isGuildOwner(interaction) or interaction.user.id in guildData["Whitelist"]:

        return True

    raise NotWhitelist
