"""
twitter.py
------------------------
TwitterAPIの認証に必要な設定を司る。
"""

import json
from typing import Dict, Union

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


def create(json_text: str) -> TwitterSetting:
    """
    Jsonファイルから設定をパースしてTwitterSettingを生成する
    :param json_text: Jsonで記述された設定。
    :return: 生成されたTwitterSetting
    """
    json_type = Dict[str, Union[None, str, int]]
    json_type = Dict[str, Union[json_type, None, str, int]]

    with open("static/scheme/twitter_scheme.json") as f:
        scheme_json: json_type = json.load(f)

    raw_json: json_type = json.loads(json_text)
    validate(raw_json, scheme_json)

    raw_json.setdefault("token", None)

    return TwitterSetting(
        raw_json["consumer_api_key"],
        raw_json["consumer_api_secret_key"],
        raw_json["access_token"],
        raw_json["access_token_secret"],
    )
