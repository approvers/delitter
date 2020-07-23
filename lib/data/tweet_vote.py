"""
tweet_vote.py
------------------------
ツイートの投票を司るクラスが入っている。
"""
import math
import random

import discord

from lib.settings.judge_standard import JudgeStandard


class TweetVote:
    """
    ツイートの投票。
    """

    def __init__(self,
                 content: str,
                 author: discord.User
                 ):
        """
        投票を初期化する。
        :param content: ツイートする内容。
        :param author: 誰が投票を作成したか。
        """
        self.content = content
        self.author = author
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

    def approved(self, judge_standard: JudgeStandard) -> bool:
        """
        可決状態にあるかを確認する。
        :param judge_standard: 可決の基準。
        :return: 可決されたどうか。可決された場合はTrueを返す。
        """
        if (self.approves + self.denys) < judge_standard.required_total:
            return False

        return self.get_approval_rate() >= judge_standard.required_rate

    def to_embed(self) -> discord.Embed:
        """
        TweetVoteをDiscordのメッセージに埋め込める形に変換する。
        :return: Embed。
        """

        # 可決率を計算する。
        approve_rate = self.get_approval_rate()

        # embedを組み立てる
        embed = discord.Embed()
        embed.title = "†ツイート審議待ち†"
        embed.description = "以下のリアクションから投票してください。\nリアクション全部消したらメス堕ちさせるからな"
        embed.colour = (random.randint(127, 255) << 16) + (random.randint(127, 255) << 8) + random.randint(127, 255)

        embed.add_field(
            name="ツイート内容",
            value="```{}```".format(self.content),
            inline=False
        )
        embed.add_field(
            name="ツイートしたい人",
            value="{} (`{}`)".format(self.author.display_name, self.author.name),
            inline=False
        )
        embed.add_field(
            name="投票状況",
            value=":thumbsup: {}/{} :thumbsdown: ({}%)".format(
                self.approves,
                self.denys,
                approve_rate
            ),
            inline=False
        )

        # 返す。
        return embed

    def __str__(self) -> str:
        """
        文字列izeする。
        :return: 文字列と化したTweetVote
        """
        return "{}\nAuthored by: {}".format(self.content, self.author)

