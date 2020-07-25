import random

import discord

from lib.data.tweet_vote import TweetVote


def create_tweet_vote_embed(tweet_vote: TweetVote) -> discord.Embed:
    """
    TweetVoteをDiscordのメッセージに埋め込める形に変換する。
    :param tweet_vote: 投票。
    :return: Embed。
    """

    # 可決率を計算する。
    approve_rate = tweet_vote.get_approval_rate()

    # embedを組み立てる
    embed = discord.Embed()
    embed.title = "†ツイート審議待ち†"
    embed.description = "以下のリアクションから投票してください。\nリアクション全部消したらメス堕ちさせるからな"
    embed.colour = (random.randint(127, 255) << 16) + (random.randint(127, 255) << 8) + random.randint(127, 255)

    embed.add_field(
        name="ツイート内容",
        value="```{}```".format(tweet_vote.content),
        inline=False
    )
    embed.add_field(
        name="ツイートしたい人",
        value="{} (`{}`)".format(tweet_vote.author_nickname, tweet_vote.author_name),
        inline=False
    )
    embed.add_field(
        name="投票状況",
        value=":thumbsup: {}/{} :thumbsdown: ({}%)".format(
            tweet_vote.approves,
            tweet_vote.denys,
            approve_rate
        ),
        inline=False
    )

    # 返す。
    return embed
