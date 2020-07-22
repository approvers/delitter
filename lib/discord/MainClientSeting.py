import json
import os

from typing.io import TextIO


class MainClientSetting:

    def __init__(self,
                 token: str,
                 activity_channel_id: int,
                 ):
        """
        MainClientクラスで使用する設定を保持するクラス。
        :param token: ログインに使用するトークン。
                      Noneが渡された場合はDISCORD_TOKEN環境変数からの読み出しを試みる。
        :param activity_channel_id: 動作するチャンネル。
        """

        if token is None and "DISCORD_TOKEN" not in os.environ:
            raise RuntimeError("Neither argument 'token' nor DISCORD_TOKEN are set!")

        self.token = os.environ["DISCORD_TOKEN"] if token is None else token
        self.activity_channel_id = activity_channel_id

    @classmethod
    def load_from_json(cls, file: TextIO):
        """
        Jsonファイルから設定をパースしてMainClientSettingを生成する
        :param file: Jsonファイルを参照しているIO。
        :return: 生成されたMainClientSetting
        """
        raw_json: dict = json.load(file)
        raw_json.setdefault("token", None)

        return MainClientSetting(
            raw_json["token"],
            raw_json["activity_channel_id"]
        )
