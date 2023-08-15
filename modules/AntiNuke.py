from discord import Member

from modules.core.PPUserModule import PPUserModule


class AntiNuke(PPUserModule):

    def __init__(self):

        super().__init__(
            enabled=True
        )

    async def _punishment(self, member: Member) -> None:

        try:

            if member.bot:

                await member.kick()

            else:

                await member.ban()

        except Exception:

            pass
