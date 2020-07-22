from abc import ABCMeta, abstractmethod

import discord

from lib.discord import Client
from lib.discord.command.CommandInfo import CommandInfo


class ABCCommand(metaclass=ABCMeta):
    """
    コマンドの抽象クラス。
    """

    @abstractmethod
    def get_command_info(self) -> CommandInfo:
        """
        コマンドの情報を取得する。
        :return: コマンドの情報が代入されたCommandInfo
        """
        pass

    @abstractmethod
    def parse_command(self, text: str, author: discord.User, client: Client):
        """
        コマンドを実行する。
        :param text: 受信したメッセージからPrefixとコマンド識別文字列を除いた文字列。
        :param author: メッセージを送信したユーザー。
        :param client: このメッセージを受信したクライアント。
        """
        pass
