import datetime

from discord import Member
from asyncio import Semaphore
from collections import defaultdict
from abc import ABC, abstractmethod

from modules.core.Module import Module


class PPUserModule(Module, ABC):

    def __init__(self, enabled: bool):

        self.__data: defaultdict = defaultdict(lambda: [])
        self.__semaphore: Semaphore = Semaphore(1)

        super().__init__(
            enabled=enabled
        )

    async def new_element(self, member: Member) -> None:

        strUserId: str = str(member.id)
        currentDate: datetime.datetime = datetime.datetime.utcnow()

        async with self.__semaphore:

            self.__data[strUserId] = [
                element for element in self.__data[strUserId]
                if element["expirationDate"] >= currentDate.timestamp()
            ]

            self.__data[strUserId].append({
                "expirationDate": (currentDate + datetime.timedelta(seconds=5)).timestamp()
            })

            if len(self.__data[strUserId]) > 5:

                self.__data[strUserId] = []

                self.__semaphore.release()

                await self._punishment(member)

    @abstractmethod
    async def _punishment(self, member: Member) -> None:

        pass
