from twitter import *

from lib.logging.logger import log
from lib.settings.twitter import TwitterSetting


class Tweeter:

    def __init__(self, setting: TwitterSetting):
        self.twitter = Twitter(
            auth=OAuth(
                setting.access_token,
                setting.access_secret_token,
                setting.consumer_key,
                setting.consumer_secret_key
            )
        )

    def tweet(self, content: str):
        log("twitter-helper", "以下の内容でツイートが行われました: {}".format(content))
        self.twitter.statuses.update(status=content)
