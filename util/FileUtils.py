import random

from string import digits


class FileUtils:

    @staticmethod
    def randomID() -> str:

        return "".join(random.choices(digits, k=12))
