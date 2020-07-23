from typing import Dict

from lib.data.TweetVote import TweetVote


class PendingTweetsManager:
    """
    進行中の投票をIDと関連付けて持っておくクラス。シングルトン。
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(PendingTweetsManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        初期化する。すでにインスタンスが存在している場合は初期化しない。
        """
        if not hasattr(self, "pending_tweets"):
            self.pending_tweets: Dict[int, TweetVote] = {}

    def add(self, tweet_id: int, content: TweetVote):
        """
        投票を登録する。
        :param tweet_id: 投票のID。
        :param content: 投票。
        :return:
        """
        self.pending_tweets[tweet_id] = content

    def get(self, tweet_id: int):
        """
        投票を取得する。
        :param tweet_id: 検索するID。
        :return: 見つかった場合は投票。見つからなければNone。
        """
        if tweet_id not in self.pending_tweets:
            return None
        return self.pending_tweets[tweet_id]

    def delete(self, tweet_id):
        """
        投票を削除する。
        :param tweet_id: 検索するID。
        """
        del self.pending_tweets[tweet_id]

