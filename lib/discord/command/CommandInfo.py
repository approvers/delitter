class CommandInfo:

    def __init__(
            self,
            identify: str,
            args_format: str,
            name: str,
            description: str
    ):
        self.identify = identify
        self.args_format = args_format
        self.name = name
        self.description = description
