"""
tweets_vote_record.py
------------------------
投票を保存するクラスが入っている。
"""
import threading
from typing import Dict

from lib.data.tweet_vote import TweetVote


class TweetsVoteRecord:
    """
    進行中の投票をIDと関連付けて持っておくクラス。
    処理は全てスレッドセーフ。
    """
    __PENDING_TWEETS_LIST: Dict[int, TweetVote] = {}
    __THREAD_LOCK: threading.Lock = threading.Lock()

    @staticmethod
    def add(tweet_id: int, content: TweetVote):
        """
        投票を登録する。
        :param tweet_id: 投票のID。
        :param content: 投票。
        """
        with TweetsVoteRecord.__THREAD_LOCK:
            TweetsVoteRecord.__PENDING_TWEETS_LIST[tweet_id] = content

    @staticmethod
    def get(tweet_id: int):
        """
        投票を取得する。
        :param tweet_id: 検索するID。
        :return: 見つかった場合は投票。見つからなければNone。
        """
        with TweetsVoteRecord.__THREAD_LOCK:
            if tweet_id not in TweetsVoteRecord.__PENDING_TWEETS_LIST:
                return None
            return TweetsVoteRecord.__PENDING_TWEETS_LIST[tweet_id]

    @staticmethod
    def delete(tweet_id):
        """
        投票を削除する。
        :param tweet_id: 検索するID。
        """
        with TweetsVoteRecord.__THREAD_LOCK:
            del TweetsVoteRecord.__PENDING_TWEETS_LIST[tweet_id]

