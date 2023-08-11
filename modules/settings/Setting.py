import abc

import discord

from typing import Any
from abc import ABC


class Setting(ABC):

    def __init__(self, name: str, description: str, value: Any):

        self.name: str = name
        self.description: str = description
        self.value: Any = value

    @abc.abstractmethod
    def embedRender(self, embed: discord.Embed) -> None:

        pass
