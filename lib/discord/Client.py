import discord

from lib.discord.MainClientSeting import MainClientSetting


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
        self.run(self.setting.token)

    async def on_ready(self):
        self.activity_channel = self.get_channel(self.setting.activity_channel_id)

        if self.activity_channel is None:
            raise RuntimeError("Activity channel is not found! Check your \"activity_channel_id\" value.")

        await self.activity_channel.send("***†Delitter Ready†***")




