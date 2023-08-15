from discord import Embed, Color
from datetime import datetime


class EmbedUtils:

    @staticmethod
    def basicEmbed(title: str = None, description: str = None) -> Embed:

        em = Embed(
            title=title, description=description,
            color=Color.from_rgb(47, 49, 54),
            timestamp=datetime.utcnow()
        )

        return em
