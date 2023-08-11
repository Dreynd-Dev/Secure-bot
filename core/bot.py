import os
import discord

from collections import defaultdict
from typing import Type

from file.file import File
from commands.core.Context import Context


class Bot(discord.Bot):

    def __init__(self):

        self.file: File = File()

        self.instances: defaultdict = defaultdict(lambda: defaultdict(lambda: None))

        super().__init__(
            context=Context,
            intents=discord.Intents.all()
        )

    def getInstance(self, guildID: int, module: Type):

        instance = self.instances[str(guildID)][module.__name__]

        if instance is None:

            instance = module(self, guildID)
            self.instances[str(guildID)][module.__name__] = instance

        return instance

    def __load_cogs(self):

        for filename in os.listdir("commands"):

            if filename.endswith(".py"):

                self.load_extension(f"commands.{filename[:-3]}")

        for filename in os.listdir("events"):

            if filename.endswith(".py"):

                self.load_extension(f"events.{filename[:-3]}")

    async def run(self):

        self.__load_cogs()

        await self.file.load()

        await self.start("")
