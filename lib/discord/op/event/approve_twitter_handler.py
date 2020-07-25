"""
approve_twitter_handler.py
------------------------
可決されたときのツイッター周りの処理を司る。
"""
import discord

from lib.data.tweet_votes_record import TweetsVoteRecord
from lib.discord.op.event.approve_event import ApproveEvent
from lib.twitter.tweeter import Tweeter


class ApproveTwitterHandler(ApproveEvent):
    """
    可決時のツイート処理をする。
    """

    def __init__(self, tweeter: Tweeter):
        self.tweeter = tweeter

    async def on_approved(self, message: discord.Message, vote_record: TweetsVoteRecord):
        self.tweeter.tweet(vote_record.get(message.id).content)
