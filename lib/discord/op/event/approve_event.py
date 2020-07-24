"""
approve_event.py
------------------------
投票が可決されたときに発火される関数が入っている。
"""
from abc import ABCMeta, abstractmethod

import discord

from lib.data.tweet_votes_record import TweetsVoteRecord


class ApproveEvent(metaclass=ABCMeta):

    @abstractmethod
    async def on_approved(self, message: discord.Message, vote_record: TweetsVoteRecord):
        """
        リアクションが可決されたときに発火されるイベント。
        Discord周りを処理する。
        :param message: 該当するメッセージ。
        :param vote_record: ツイートの投票のレコード。
        """
        pass
