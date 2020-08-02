"""
discord.py
------------------------
DiscordのBot周りの設定を司る。
"""

import json
import os
from typing import Dict, Union

from jsonschema import validate
from typing.io import TextIO


class DiscordSetting:
    """
    Botの設定。
    """

    def __init__(
            self,
            token: str,
            activity_channel_id: int,
            prefix: str,
            suffrage_role_id: int,
            emoji_ids: Dict[str, int],
            approve_rate: int
    ):
        """
        MainClientクラスで使用する設定を保持するクラス。
        :param token: ログインに使用するトークン。
                      Noneが渡された場合はDISCORD_TOKEN環境変数からの読み出しを試みる。
        :param activity_channel_id: 動作するチャンネル。
        :param prefix: Botのプレフィックス。
        :param suffrage_role_id: 参政権ロールのID。
        :param emoji_ids: 投票に使用する絵文字のID。
        :param approve_rate: 可決に必要な、総有権者数に対する可決率。
        """

        if token is None and "DISCORD_TOKEN" not in os.environ:
            raise RuntimeError("Neither argument 'token' nor DISCORD_TOKEN are set!")

        self.token = os.environ["DISCORD_TOKEN"] if token is None else token
        self.activity_channel_id = activity_channel_id
        self.prefix = prefix
        self.suffrage_role_id = suffrage_role_id
        self.emoji_ids = emoji_ids
        self.approve_rate = approve_rate


def create(json_text: str) -> DiscordSetting:
    """
    Jsonファイルから設定をパースしてDiscordSettingを生成する
    :param json_text: Jsonで記述された設定。
    :return: 生成されたDiscordSetting
    """
    json_type = Dict[str, Union[None, str, int]]
    json_type = Dict[str, Union[json_type, None, str, int]]

    with open("static/scheme/discord_scheme.json") as f:
        scheme_json: json_type = json.load(f)

    raw_json: json_type = json.loads(json_text)
    validate(raw_json, scheme_json)

    raw_json.setdefault("token", None)

    return DiscordSetting(
        raw_json["token"],
        raw_json["activity_channel_id"],
        raw_json["prefix"],
        raw_json["suffrage_role_id"],
        raw_json["emoji_ids"],
        raw_json["approve_rate"]
    )
