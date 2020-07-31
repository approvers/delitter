"""
tweet_vote.py
------------------------
ツイートの投票を司るクラスが入っている。
"""
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
        """
        self.content = content
        self.author_id = author.id
        self.author_nickname = author.display_name
        self.author_name = author.name
        self.required_approve_count = required_approve_count
        self.approves = 0
        self.denys = 0

    def __str__(self) -> str:
        """
        文字列izeする。
        :return: 文字列と化したTweetVote
        """
        return "{}\nAuthored by: {}".format(self.content, self.author_name)
