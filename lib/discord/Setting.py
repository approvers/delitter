import json
import os
from typing import Dict

from typing.io import TextIO


class Setting:

    def __init__(self,
                 token: str,
                 activity_channel_id: int,
                 prefix: str,
                 guild_id: int,
                 suffrage_role_id: int,
                 emoji_ids: Dict[str, int],
                 ):
        """
        MainClientクラスで使用する設定を保持するクラス。
        :param token: ログインに使用するトークン。
                      Noneが渡された場合はDISCORD_TOKEN環境変数からの読み出しを試みる。
        :param activity_channel_id: 動作するチャンネル。
        :param prefix: Botのプレフィックス。
        """

        if token is None and "DISCORD_TOKEN" not in os.environ:
            raise RuntimeError("Neither argument 'token' nor DISCORD_TOKEN are set!")

        self.token = os.environ["DISCORD_TOKEN"] if token is None else token
        self.activity_channel_id = activity_channel_id
        self.prefix = prefix
        self.guild_id = guild_id
        self.suffrage_role_id = suffrage_role_id
        self.emoji_ids = emoji_ids

    @classmethod
    def load_from_json(cls, file: TextIO):
        """
        Jsonファイルから設定をパースしてMainClientSettingを生成する
        :param file: Jsonファイルを参照しているIO。
        :return: 生成されたMainClientSetting
        """
        raw_json: dict = json.load(file)
        raw_json.setdefault("token", None)

        return Setting(
            raw_json["token"],
            raw_json["activity_channel_id"],
            raw_json["prefix"],
            raw_json["guild_id"],
            raw_json["suffrage_role_id"],
            raw_json["emoji_ids"]
        )
