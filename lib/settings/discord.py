"""
discord.py
------------------------
DiscordのBot周りの設定を司る。
"""

import json
import os
from typing import Dict

from jsonschema import validate
from typing.io import TextIO

from lib.data.judge_standard import JudgeStandard


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
            judge_standard: JudgeStandard,
    ):
        """
        MainClientクラスで使用する設定を保持するクラス。
        :param token: ログインに使用するトークン。
                      Noneが渡された場合はDISCORD_TOKEN環境変数からの読み出しを試みる。
        :param activity_channel_id: 動作するチャンネル。
        :param prefix: Botのプレフィックス。
        :param suffrage_role_id: 参政権ロールのID。
        :param emoji_ids: 投票に使用する絵文字のID。
        :param judge_standard: 可決となるための基準。
        """

        if token is None and "DISCORD_TOKEN" not in os.environ:
            raise RuntimeError("Neither argument 'token' nor DISCORD_TOKEN are set!")

        self.token = os.environ["DISCORD_TOKEN"] if token is None else token
        self.activity_channel_id = activity_channel_id
        self.prefix = prefix
        self.suffrage_role_id = suffrage_role_id
        self.emoji_ids = emoji_ids
        self.judge_standard = judge_standard


def create(file: TextIO) -> DiscordSetting:
    """
    Jsonファイルから設定をパースしてDiscordSettingを生成する
    :param file: Jsonファイルを参照しているIO。
    :return: 生成されたDiscordSetting
    """

    with open("static/scheme/discord_scheme.json") as f:
        scheme_json: dict = json.load(f)

    raw_json: dict = json.load(file)
    validate(raw_json, scheme_json)

    raw_json.setdefault("token", None)

    return DiscordSetting(
        raw_json["token"],
        raw_json["activity_channel_id"],
        raw_json["prefix"],
        raw_json["suffrage_role_id"],
        raw_json["emoji_ids"],
        JudgeStandard(
            raw_json["judge_standard"]["total"],
            raw_json["judge_standard"]["rate"]
        )
    )