from discord.ext.commands import CheckFailure


class NotOwner(CheckFailure):

    pass


class NotWhitelist(CheckFailure):

    pass
