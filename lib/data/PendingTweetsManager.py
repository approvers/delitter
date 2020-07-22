from typing import Dict

from lib.types.TweetContent import TweetContent


class PendingTweetsManager:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(PendingTweetsManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "pending_tweets"):
            self.pending_tweets: Dict[int, TweetContent] = {}

    def add(self, tweet_id: int, content: TweetContent):
        self.pending_tweets[tweet_id] = content

    def get(self, tweet_id: int):
        if tweet_id not in self.pending_tweets:
            return None
        return self.pending_tweets[tweet_id]

    def delete(self, tweet_id):
        del self.pending_tweets[tweet_id]

