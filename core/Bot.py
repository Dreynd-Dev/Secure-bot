import os
import discord

from discord.ext import commands
from collections import defaultdict
from typing import Type

from files.core.Data import Data
from modules.core import Module


class Bot(commands.AutoShardedBot):

    def __init__(self):

        self.data: Data = Data()
        self.__moduleInstances: defaultdict = defaultdict(lambda: defaultdict(lambda: None))

        super().__init__(
            command_prefix="",
            intents=discord.Intents.all(),
            application_id=1139575728959139880
        )

    def getModuleInstance(self, guildID: int, module: Type[Module]) -> Module:

        strGuildId: str = str(guildID)

        moduleInstance: Module = self.__moduleInstances[strGuildId][module.__name__]

        if moduleInstance is None:

            moduleInstance: Module = module()
            self.__moduleInstances[strGuildId][module.__name__]: Module = moduleInstance

        return moduleInstance

    async def __load_cogs(self) -> None:

        for filename in os.listdir("commands"):

            if filename.endswith(".py"):

                await self.load_extension(f"commands.{filename[:-3]}")

        for filename in os.listdir("events"):

            if filename.endswith(".py"):

                await self.load_extension(f"events.{filename[:-3]}")

    async def build(self) -> None:

        await self.data.load()

        await self.__load_cogs()

        await self.start("")
