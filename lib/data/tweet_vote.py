"""
tweet_vote.py
------------------------
ツイートの投票を司るクラスが入っている。
"""
import math

import discord


class TweetVote:
    """
    ツイートの投票。
    """

    def __init__(
            self,
            content: str,
            author: discord.Member,
            required_approve_count: int
    ):
        """
        投票を初期化する。
        :param content: ツイートする内容。
        :param author: 投票を作成した人。
        :param required_approve_count: 可決に必要な票数。
        """
        self.content = content
        self.author_id = author.id
        self.author_nickname = author.display_name
        self.author_name = author.name
        self.required_approve_count = required_approve_count
        self.approves = 0
        self.denys = 0

    def get_approval_rate(self) -> int:
        """
        投票の可決率を計算する。
        総票数がゼロの場合は0とする。
        :return: 投票の可決率。
        """
        if (self.approves + self.denys) == 0:
            return 0

        return math.floor(self.approves / (self.approves + self.denys) * 100)

    def is_approved(self) -> bool:
        """
        可決状態にあるかを確認する。
        :return: 可決されたどうか。可決された場合はTrueを返す。
        """
        return self.approves >= self.required_approve_count

    def __str__(self) -> str:
        """
        文字列izeする。
        :return: 文字列と化したTweetVote
        """
        return "{}\nAuthored by: {}".format(self.content, self.author_name)
