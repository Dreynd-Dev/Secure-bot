from discord import Member
from datetime import timedelta

from modules.core.PPUserModule import PPUserModule


class AntiSpam(PPUserModule):

    def __init__(self):

        super().__init__(
            enabled=True
        )

    async def _punishment(self, member: Member) -> None:

        try:

            await member.timeout(timedelta(days=3))

        except Exception:

            pass
