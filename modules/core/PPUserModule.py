import discord
import datetime

from asyncio import Semaphore
from abc import ABC, abstractmethod

from modules.core.Module import Module


class PPUserModule(Module, ABC):

    def __init__(self, enabled: bool, maxElements: int, expirationTime: int):

        super().__init__(
            enabled=enabled
        )

        self.maxElements = maxElements
        self.expirationTime = expirationTime

        self.data: dict = {}
        self.semaphore: Semaphore = Semaphore()

    async def new_element(self, member: discord.Member):

        userID = member.id

        current_datetime = datetime.datetime.utcnow()

        if str(userID) not in self.data:

            self.data[str(userID)] = []

        async with self.semaphore:

            self.data[str(userID)] = [
                element for element in self.data[str(userID)]
                if element["expiration"] >= current_datetime.timestamp()
            ]

            newElement = {
                "creation": current_datetime.timestamp(),
                "expiration": (current_datetime + datetime.timedelta(seconds=self.expirationTime)).timestamp()
            }

            self.data[str(userID)].append(newElement)

            if len(self.data[str(userID)]) > self.maxElements:

                self.data.pop(str(userID))

                self.semaphore.release()

                await self._punishment(member)

    @abstractmethod
    async def _punishment(self, member: discord.Member):

        pass
