class Module:

    def __init__(self, enabled: bool):

        self.enabled: bool = enabled
        self.options: dict = {}

    def toggle(self) -> None:

        self.enabled = not self.enabled
