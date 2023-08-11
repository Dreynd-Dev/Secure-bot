from discord import commands


class Context(commands.ApplicationContext):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
