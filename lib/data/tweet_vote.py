"""
tweet_vote.py
------------------------
ツイートの投票を司るクラスが入っている。
"""
import math

import discord

from lib.data.judge_standard import JudgeStandard


class TweetVote:
    """
    ツイートの投票。
    """

    def __init__(
            self,
            content: str,
            author: discord.Member
     ):
        """
        投票を初期化する。
        :param content: ツイートする内容。
        :param author: 投票を作成した人。
        """
        self.content = content
        self.author_id = author.id
        self.author_nickname = author.display_name
        self.author_name = author.name
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

    def is_approved(self, judge_standard: JudgeStandard) -> bool:
        """
        可決状態にあるかを確認する。
        :param judge_standard: 可決の基準。
        :return: 可決されたどうか。可決された場合はTrueを返す。
        """
        if (self.approves + self.denys) < judge_standard.required_total:
            return False

        return self.get_approval_rate() >= judge_standard.required_rate

    def __str__(self) -> str:
        """
        文字列izeする。
        :return: 文字列と化したTweetVote
        """
        return "{}\nAuthored by: {}".format(self.content, self.author_name)
