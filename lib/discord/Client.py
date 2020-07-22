import discord

from lib.discord.MainClientSeting import MainClientSetting
from lib.logging.Logger import log


class MainClient(discord.Client):
    """
    DiscordのBot。
    """

    def __init__(self, setting: MainClientSetting):
        """
        指定した設定でクライアントを初期化する。
        :param setting: Botに使用する設定。
        """
        super(MainClient, self).__init__()
        self.setting: MainClientSetting = setting
        self.activity_channel: discord.TextChannel = None

    def launch(self):
        """
        Botを起動する。
        Botが何らかの理由で終了するまで処理は停止する。
        """
        log("client", "Login started")
        self.run(self.setting.token)

    async def on_ready(self):
        log("client", "Bot ready. Validating condition...")
        self.activity_channel = self.get_channel(self.setting.activity_channel_id)

        if self.activity_channel is None:
            raise RuntimeError("Activity channel is not found! Check your \"activity_channel_id\" value.")

        log("client", "No errors found! Greeting to server.")
        await self.activity_channel.send("***†Delitter Ready†***")




