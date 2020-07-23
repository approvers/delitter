"""
abc_command.py
------------------------
コマンドの基底となるクラスが入っている。
"""
from abc import ABCMeta, abstractmethod

import discord

from lib.data.tweet_votes_record import TweetsVoteRecord
from lib.discord.op.command.command_property import CommandProperty
from lib.settings.setting import Setting


class ABCCommand(metaclass=ABCMeta):
    """
    コマンドの抽象クラス。
    """

    @abstractmethod
    def __init__(self, guild: discord.Guild, setting: Setting, vote_record: TweetsVoteRecord):
        """
        インスタンスを初期化する。
        初期化はBotのログイン直後に行われる。
        :param guild: Botが所属するギルド。
        :param setting: Botの設定。
        """
        pass

    @abstractmethod
    def get_command_info(self) -> CommandProperty:
        """
        コマンドの情報を取得する。
        :return: コマンドの情報が代入されたCommandInfo
        """
        pass

    @abstractmethod
    def parse_command(self, text: str, message: discord.Message):
        """
        コマンドを実行する。
        :param text: 受信したメッセージからPrefixとコマンド識別文字列を除いた文字列。
        :param message: メッセージの情報。
        """
        pass

    def __str__(self):
        """
        文字列で自己表現する。
        :return: 自己表現の結果。
        """
        return str(self.get_command_info())
