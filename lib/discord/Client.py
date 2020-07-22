from typing import Dict

import discord

from lib.discord.MainClientSeting import MainClientSetting
from lib.discord.command.ABCCommand import ABCCommand
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
        self.commands: Dict[str, ABCCommand] = {}

    def launch(self):
        """
        Botを起動する。
        Botが何らかの理由で終了するまで処理は停止する。
        """
        log("client-login", "ログイン処理を開始します。")
        self.run(self.setting.token)

    def add_command(self, command: ABCCommand):
        self.commands[command.get_command_info().identify] = command

    async def on_ready(self):
        log("client-login", "ログインに成功しました。適切な設定が行われているか確認しています。")
        self.activity_channel = self.get_channel(self.setting.activity_channel_id)

        if self.activity_channel is None:
            raise RuntimeError("Activity channel is not found! Check your \"activity_channel_id\" value.")

        log("client-login", "設定に問題はありませんでした。起動メッセージを送信します…")
        await self.activity_channel.send("***†Delitter Ready†***")

    async def on_message(self, message: discord.Message):
        if message.author.bot or message.channel.id != self.setting.activity_channel_id:
            log("client-msg", "メッセージはBotからのものか、Activity Channelではないところで発言されたものでした。無視します！")
            return

        if not message.content.startswith(self.setting.prefix):
            log("client-msg", "メッセージは処理対象でしたが、Prefix「{}」がありませんでした。無視します！".format(self.setting.prefix))
            return

        log("client-msg", "処理対象のメッセージを受信しました:\n{}".format(message.content))

        cmd_identity = message.content.split(" ")[0][len(self.setting.prefix):]
        if cmd_identity not in self.commands:
            log("client-msg", "コマンドが見つかりませんでした: 「{}」".format(cmd_identity))
            await self.activity_channel.send("知らないコマンドが出てきました:thinking:")
            return

        await self.commands[cmd_identity].parse_command(
            message.content[:len(self.setting.prefix) + len(cmd_identity)],
            message
        )





