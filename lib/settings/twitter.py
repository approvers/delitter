"""
twitter.py
------------------------
TwitterAPIの認証に必要な設定を司る。
"""

import json

from jsonschema import validate
from typing.io import TextIO


class TwitterSetting:
    """
    Twitter認証にまつわる設定。
    """

    def __init__(
            self,
            consumer_api_key: str,
            consumer_api_secret_key: str,
            access_token: str,
            access_token_secret: str,
    ):
        """
        TwitterHelperクラスで使用する設定。
        :param consumer_api_key: Consumer API Key.
        :param consumer_api_secret_key: Consumer API Secret Key.
        :param access_token: Access Token.
        :param access_token_secret: Access Token Secret.
        """
        self.consumer_key = consumer_api_key
        self.consumer_secret_key = consumer_api_secret_key
        self.access_token = access_token
        self.access_secret_token = access_token_secret


def create_twitter_setting_from_json(file: TextIO) -> TwitterSetting:
    """
    Jsonファイルから設定をパースしてTwitterSettingを生成する
    :param file: Jsonファイルを参照しているIO。
    :return: 生成されたTwitterSetting
    """

    with open("static/scheme/twitter_scheme.json", mode="r") as f:
        scheme_json: dict = json.load(f)

    raw_json: dict = json.load(file)
    validate(raw_json, scheme_json)

    raw_json.setdefault("token", None)

    return TwitterSetting(
        raw_json["consumer_api_key"],
        raw_json["consumer_api_secret_key"],
        raw_json["access_token"],
        raw_json["access_token_secret"],
    )
