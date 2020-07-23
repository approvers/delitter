class CommandProperty:
    """
    コマンドの情報を保持するクラス。
    """

    def __init__(
            self,
            identify: str,
            args_format: str,
            name: str,
            description: str
    ):
        """
        初期化する。
        :param identify: コマンドを実行するための識別文字。
        :param args_format: 引数の形式を説明する文字列。
        :param name: コマンドの名前。
        :param description: コマンドが具体的に何をするか。
        """
        self.identify = identify
        self.args_format = args_format
        self.name = name
        self.description = description
