import datetime

import discord


class EmbedUtils:

    @staticmethod
    def basicEmbed(title: str = None, description: str = None):

        embed = discord.Embed(
            title=title, description=description,
            color=discord.Color.from_rgb(47, 49, 54),
            timestamp=datetime.datetime.utcnow()
        )

        return embed