"""
tweets_vote_record.py
------------------------
投票を保存するクラスが入っている。
"""
import copy
import threading
from typing import Dict, Optional

from lib.data.tweet_vote import TweetVote


class TweetsVoteRecord:
    """
    進行中の投票をIDと関連付けて持っておくクラス。
    処理は全てスレッドセーフ。
    """
    def __init__(self):
        self.pending_tweets_list: Dict[int, TweetVote] = {}
        self.thread_lock: threading.Lock = threading.Lock()

    def add(self, tweet_id: int, content: TweetVote):
        """
        投票を登録する。
        :param tweet_id: 投票のID。
        :param content: 投票。
        """
        with self.thread_lock:
            if tweet_id in self.pending_tweets_list:
                raise RuntimeError("投票IDが重複しました。もう一度登録してください。")
            self.pending_tweets_list[tweet_id] = content

    def get(self, tweet_id: int) -> Optional[TweetVote]:
        """
        投票を取得する。
        :param tweet_id: 検索するID。
        :return: 見つかった場合は投票。見つからなければNone。
        """
        with self.thread_lock:
            if tweet_id not in self.pending_tweets_list:
                return None
            return copy.deepcopy(self.pending_tweets_list[tweet_id])

    def set(self, tweet_id: int, content: TweetVote):
        """
        投票を再登録する。
        :param tweet_id: 再登録を行う投票のID。
        :param content: 登録する投票
        """
        with self.thread_lock:
            if tweet_id not in self.pending_tweets_list:
                raise RuntimeError("Setしようとした投票が削除されています。(ID: {})".format(tweet_id))
            self.pending_tweets_list[tweet_id] = content

    def delete(self, tweet_id: int):
        """
        投票を削除する。
        :param tweet_id: 検索するID。
        """
        with self.thread_lock:
            del self.pending_tweets_list[tweet_id]
