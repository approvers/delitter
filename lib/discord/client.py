"""
client.py
------------------------
DiscordのBotとして機能するクライアントが入っている。
"""
from typing import Dict, Type, List

import discord

from lib.data.tweet_votes_record import TweetsVoteRecord
from lib.discord.op.command.abc_command import ABCCommand
from lib.discord.op.event import approve_event
from lib.discord.op.event.reaction_event import ReactionEvent
from lib.logging.logger import log
from lib.settings.setting import Setting


class MainClient(discord.Client):
    """
    DiscordのBot。
    """

    def __init__(self, setting: Setting, vote_record: TweetsVoteRecord):
        """
        指定した設定でクライアントを初期化する。
        :param setting: Botに使用する設定。
        :param vote_record: ツイートの投票を記録するレコード。
        """
        super(MainClient, self).__init__()
        self.reaction_event_handler: ReactionEvent = ReactionEvent(setting, vote_record)
        self.setting: Setting = setting
        self.vote_record: TweetsVoteRecord = vote_record
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
        """
        self.commands_type.append(command)

    async def on_ready(self):
        """
        Botが起動した際に呼ばれる。
        必要なチャンネルが存在するかを確認し、コマンドの初期化を行う。
        """
        log("client-login", "ログインに成功しました。適切な設定が行われているか確認しています。")
        self.activity_channel = self.get_channel(self.setting.activity_channel_id)

        if self.activity_channel is None:
            log("client-login", "アクティビティチャンネルが見つかりません。設定に異常があります。")
            raise RuntimeError("Activity channel is not found! Check your \"activity_channel_id\" value.")

        log("client-login", "設定に問題はありませんでした。コマンドのインスタンスを生成します…")

        for command in self.commands_type:
            log("client-login", "{} を初期化します…".format(command.__name__))
            command_instance = command(self.activity_channel.guild, self.setting, self.vote_record)
            self.commands[command_instance.get_command_info().identify] = command_instance

        log("client-login", "問題は発生しませんでした。起動メッセージを送信します…")
        await self.activity_channel.send("***†Delitter Ready†***")

    async def on_message(self, message: discord.Message):
        """
        メッセージを受信したときに発火されるイベント。
        処理対象のメッセージであるかを確認し、適切なコマンドを実行する。
        :param message: 受信したメッセージの情報。
        """

        # 処理対象のメッセージかを確認する
        if message.author.bot or message.channel.id != self.setting.activity_channel_id:
            log("client-msg", "メッセージはBotからのものか、Activity Channelではないところで発言されたものでした。無視します！")
            return

        if not message.content.startswith(self.setting.prefix):
            log("client-msg", "メッセージは処理対象でしたが、Prefix「{}」がありませんでした。無視します！".format(self.setting.prefix))
            return

        log("client-msg", "処理対象のメッセージを受信しました:\n{}".format(message.content))

        # コマンドをパースする
        cmd_header = message.content.split(" ")[0]
        cmd_identity = cmd_header[len(self.setting.prefix):]

        if cmd_identity in ["", "help"]:
            # コマンドが指定されないか、helpの場合はhelpを送信する
            await message.channel.send(self.get_help_message())
            return

        if cmd_identity not in self.commands:
            # コマンドが見つからない
            log("client-msg", "コマンドが見つかりませんでした: 「{}」".format(cmd_identity))
            await self.activity_channel.send("知らないコマンドが出てきました:thinking:")
            return

        # コマンドを実行する
        await self.commands[cmd_identity].parse_command(
            message.content[len(cmd_header) + 1:],
            message
        )

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        """
        リアクションが追加されたときに発火されるイベント。
        :param reaction: リアクションが追加された対象のメッセージの、現在のリアクションの状態
        :param user: 誰「が」リアクションを追加したか (who)
        """
        approved = await self.reaction_event_handler.on_reaction_add(reaction, user)
        if approved:
            await approve_event.on_approved(reaction.message, self.vote_record)
            # TODO: ツイートする

    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.Member):
        """
        リアクションが削除されたときに発火されるイベント。
        :param reaction: リアクションが削除された対象のメッセージの、現在のリアクションの状態
        :param user: 誰「の」リアクションが削除されたか (whose)
        """
        await self.reaction_event_handler.on_reaction_remove(reaction, user)

    async def on_reaction_clear(self, message: discord.Message, reactions: List[discord.Reaction]):
        """
        リアクションが全て削除されたときに発火されるイベント。
        :param message: 対象のメッセージ。
        :param reactions: 削除されたリアクションの情報。
        :return:
        """
        await self.reaction_event_handler.on_reaction_clear(message)

    def get_help_message(self):
        """
        ヘルプメッセージを取得する。
        :return: ヘルプメッセージ。
        """
        help_message = "***†Delitter†***\nツイートを審議するためのBotです。"
        for cmd in self.commands.values():
            help_message += str(cmd)
        return help_message




