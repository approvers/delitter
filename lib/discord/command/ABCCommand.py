from abc import ABCMeta, abstractmethod

import discord

from lib.discord.Setting import Setting
from lib.discord.command.CommandInfo import CommandInfo


class ABCCommand(metaclass=ABCMeta):
    """
    コマンドの抽象クラス。
    """

    @abstractmethod
    def __init__(self, guild: discord.Guild, setting: Setting):
        """
        インスタンスを初期化する。
        初期化はBotのログイン直後に行われる。
        :param guild: Botが所属するギルド。
        :param setting: Botの設定。
        """
        pass

    @abstractmethod
    def get_command_info(self) -> CommandInfo:
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
