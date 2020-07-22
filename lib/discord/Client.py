from typing import Dict, Type, List

import discord

from lib.discord.op.command.ABCCommand import ABCCommand
from lib.discord.op.event import ReactionEvent, ApproveEvent
from lib.logging.Logger import log
from lib.settings.Setting import Setting


class MainClient(discord.Client):
    """
    DiscordのBot。
    """

    def __init__(self, setting: Setting):
        """
        指定した設定でクライアントを初期化する。
        :param setting: Botに使用する設定。
        """
        super(MainClient, self).__init__()
        self.setting: Setting = setting
        self.activity_channel: discord.TextChannel = None
        self.commands_type: List[Type[ABCCommand]] = []
        self.commands: Dict[str, ABCCommand] = {}

    def launch(self):
        """
        Botを起動する。
        Botが何らかの理由で終了するまで処理は停止する。
        """
        log("client-login", "ログイン処理を開始します。")
        self.run(self.setting.token)

    def add_command(self, command: Type[ABCCommand]):
        """
        実行対象のコマンドを登録する。
        :param command: 実行対象のコマンドのType。
        :return:
        """
        self.commands_type.append(command)

    async def on_ready(self):
        log("client-login", "ログインに成功しました。適切な設定が行われているか確認しています。")
        self.activity_channel = self.get_channel(self.setting.activity_channel_id)

        if self.activity_channel is None:
            raise RuntimeError("Activity channel is not found! Check your \"activity_channel_id\" value.")

        log("client-login", "設定に問題はありませんでした。コマンドのインスタンスを生成します…")

        for command in self.commands_type:
            command_instance = command(self.activity_channel.guild, self.setting)
            self.commands[command_instance.get_command_info().identify] = command_instance

        log("client-login", "問題は発生しませんでした。起動メッセージを送信します…")
        await self.activity_channel.send("***†Delitter Ready†***")

    async def on_message(self, message: discord.Message):
        if message.author.bot or message.channel.id != self.setting.activity_channel_id:
            log("client-msg", "メッセージはBotからのものか、Activity Channelではないところで発言されたものでした。無視します！")
            return

        if not message.content.startswith(self.setting.prefix):
            log("client-msg", "メッセージは処理対象でしたが、Prefix「{}」がありませんでした。無視します！".format(self.setting.prefix))
            return

        log("client-msg", "処理対象のメッセージを受信しました:\n{}".format(message.content))

        cmd_header = message.content.split(" ")[0]
        cmd_identity = cmd_header[len(self.setting.prefix):]

        if cmd_identity in ["", "help"]:
            await message.channel.send(self.get_help_message())
            return

        if cmd_identity not in self.commands:
            log("client-msg", "コマンドが見つかりませんでした: 「{}」".format(cmd_identity))
            await self.activity_channel.send("知らないコマンドが出てきました:thinking:")
            return

        await self.commands[cmd_identity].parse_command(
            message.content[len(cmd_header) + 1:],
            message
        )

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        approved = await ReactionEvent.on_reaction_add(reaction, user, self.setting)
        if approved:
            await ApproveEvent.on_approved(reaction.message)

    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.Member):
        await ReactionEvent.on_reaction_remove(reaction, user, self.setting)

    async def on_reaction_clear(self, message: discord.Message, reactions: List[discord.Reaction]):
        await ReactionEvent.on_reaction_clear(message)

    def get_help_message(self):
        help_message = "***†Delitter†***\nツイートを審議するためのBotです。"
        for cmd in self.commands.values():
            info = cmd.get_command_info()
            help_message += "```{}{} {}\n  {}```".format(self.setting.prefix, info.identify, info.name, info.description)
        return help_message




