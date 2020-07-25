from abc import ABC

import discord

from lib.data.tweet_votes_record import TweetsVoteRecord
from lib.discord.op.event.approve_event import ApproveEvent
from lib.twitter.tweeter import Tweeter


class ApproveTwitterHandler(ApproveEvent, ABC):

    def __init__(self, tweeter: Tweeter):
        self.tweeter = tweeter

    def on_approved(self, message: discord.Message, vote_record: TweetsVoteRecord):
        self.tweeter.tweet(vote_record.get(message.id).content)