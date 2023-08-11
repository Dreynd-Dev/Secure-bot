import discord

from modules.settings.Setting import Setting


class MultiValueSetting(Setting):

    def __init__(self, name: str, description: str, value: bool, values: list):

        self.name: str = name
        self.description: str = description
        self.value = value

        self.values: list = []

        super().__init__(
            name=name,
            description=description,
            value=self.value
        )

    def embedRender(self, embed: discord.Embed) -> None:

        pass
