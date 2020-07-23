from typing import Type, List, Dict

import discord

from lib.data.tweet_votes_record import TweetsVoteRecord
from lib.discord.op.command.abc_command import ABCCommand
from lib.logging.logger import log
from lib.settings.setting import Setting


class CommandRegister:
    """
    コマンドを追加/初期化・実行するクラス。
    """

    def __init__(self, setting: Setting):
        """
        初期化する。
        :param setting: Botの設定
        """
        self.commands_type: List[Type[ABCCommand]] = []
        self.commands: Dict[str, ABCCommand] = {}
        self.setting = setting

    def add_command(self, command: Type[ABCCommand]):
        """
        実行対象のコマンドを登録する。
        :param command: 実行対象のコマンドのType。
        """
        self.commands_type.append(command)

    def initialize_commands(self, guild: discord.Guild, vote_record: TweetsVoteRecord):
        """
        登録されたコマンドを初期化する。
        :param guild: コマンドが実行されるギルド。
        :param vote_record: ツイートの投票のレコード。
        """
        for command in self.commands_type:
            log("cmd-init", "{} を初期化します…".format(command.__name__))
            command_instance = command(guild, self.setting, vote_record)
            self.commands[command_instance.get_command_info().identify] = command_instance

    async def parse_command(self, msg: discord.Message):
        """
        コマンドをパースする。
        :param msg: コマンドを実行するために発行されたメッセージ。
        """
        cmd_header = msg.content.split(" ")[0]
        cmd_identity = cmd_header[len(self.setting.prefix):]

        if cmd_identity in ["", "help"]:
            # コマンドが指定されないか、helpの場合はhelpを送信する
            await msg.channel.send(self.get_help_message())
            return

        if cmd_identity not in self.commands:
            # コマンドが見つからない
            log("cmd-parse", "コマンドが見つかりませんでした: 「{}」".format(cmd_identity))
            await msg.channel.send("知らないコマンドが出てきました:thinking:")
            return

        # コマンドを実行する
        await self.commands[cmd_identity].parse_command(
            msg.content[len(cmd_header) + 1:],
            msg
        )

    def get_help_message(self):
        """
        ヘルプメッセージを取得する。
        :return: ヘルプメッセージ。
        """
        help_message = "***†Delitter†***\nツイートを審議するためのBotです。"
        for cmd in self.commands.values():
            help_message += str(cmd)
        return help_message