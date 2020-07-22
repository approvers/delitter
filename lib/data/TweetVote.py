import math
import random

import discord


class TweetVote:

    def __init__(self,
                 content: str,
                 author: discord.User
                 ):
        self.content = content
        self.author = author
        self.approves = 0
        self.denys = 0

    def to_embed(self) -> discord.Embed:

        if (self.approves + self.denys) == 0:
            approve_rate = 0
        else:
            approve_rate = math.floor(self.approves / (self.approves + self.denys) * 100)

        embed = discord.Embed()
        embed.title = "†ツイート審議待ち†"
        embed.description = "以下のリアクションから投票してください。\nリアクション全部消したらメス堕ちさせるからな"
        embed.colour = (random.randint(127, 255) << 16) + (random.randint(127, 255) << 8) + random.randint(127, 255)

        embed.add_field(name="ツイート内容", value="```{}```".format(self.content), inline=False)
        embed.add_field(name="ツイートしたい人", value="{} (`{}`)".format(self.author.display_name, self.author.name), inline=False)
        embed.add_field(
            name="投票状況",
            value=":thumbsup: {}/{} :thumbsdown: ({}%)".format(
                self.approves,
                self.denys,
                approve_rate
            ),
            inline=False
        )

        return embed

    def __str__(self):
        return "{}\nAuthored by: {}".format(self.content, self.author)
