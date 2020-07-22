import re
import unicodedata
from abc import ABC
from math import ceil
from typing import Dict

import discord

from lib.discord.Client import MainClient
from lib.discord.command.ABCCommand import ABCCommand
from lib.discord.command.CommandInfo import CommandInfo
from lib.logging.Logger import log
from lib.types.TweetContent import TweetContent


class CreateTweetVoteCommand(ABCCommand, ABC):
    SPECIAL_CHARACTER_REGEX: re.Pattern = re.compile("<[@#:].*?>")

    def __init__(self, client: MainClient):
        super().__init__(client)
        self.pending_tweets: Dict[int, TweetContent] = {}
        self.suffrage_mention = \
            client.get_guild(client.setting.guild_id).get_role(client.setting.suffrage_role_id).mention
        self.emoji = {
            "approve": client.get_emoji(client.setting.emoji_ids["approve"]),
            "deny": client.get_emoji(client.setting.emoji_ids["deny"])
        }

    def get_command_info(self) -> CommandInfo:
        return CommandInfo(
            identify="create",
            args_format="(ツイートの内容)",
            name="ツイートを作成する",
            description="ツイートしたい内容を"
        )

    async def parse_command(self, text: str, message: discord.Message):
        log("command-create", "ツイートの作成コマンドを受信しました。")

        # ツイート内容に問題がないか確認する
        error_message = validate_tweet(text)
        if error_message != "":
            await message.channel.send(error_message)
            return

        # ツイート内容のデータを生成する
        tweet_content = TweetContent(text, message.author)

        # 投票用のEmbedを作成する
        embed = tweet_content.to_embed()
        embed.set_footer(text="†ACQUIRING ID IN PROGRESS†")
        sent_message: discord.Message = await message.channel.send("IDを取得しています…", embed=embed)

        # 送信して得たIDをEmbedに埋め込む(編集)
        new_embed = sent_message.embeds[0]
        new_embed.set_footer(text="ID: {}".format(sent_message.id))
        await sent_message.edit(content="リアクションを設定しています…", embed=new_embed)

        # リアクションを設定する
        await sent_message.add_reaction(self.emoji["approve"])
        await sent_message.add_reaction(self.emoji["deny"])

        # ステータスメッセージを設定する
        await sent_message.edit(content="{}の皆さん、投票のお時間ですわよ！".format(self.suffrage_mention), embed=new_embed)

        # 保存してDone
        self.pending_tweets[sent_message.id] = tweet_content
        log("command-create", "以下のコンテンツを登録しました:\n{}".format(tweet_content))


def validate_tweet(text) -> str:
    """
    ツイート内容に問題がないか確認する
    :param text: 確認するツイート内容。
    :return: 問題が会った場合はエラーメッセージ。問題なければ空文字が返ってくる。
    """
    apparent_len = get_apparently_length(text)
    if apparent_len > 240:
        log("command-create", "文字列が長すぎました。({} > 240)".format(apparent_len))
        return "テキストが長すぎるみたいです:thinking:\n" \
               "{}文字あって{}文字オーバーしてるので削ってみてください。" \
            .format(ceil(apparent_len / 2), ceil(apparent_len / 2 - 240))

    if apparent_len < 2:
        log("command-create", "文字列が極端に短いです。({} < 2)".format(apparent_len))
        return "文字列が極端に短いみたいです:thinking:\n" \
               "1文字(英数字の場合は2文字です)も入ってないみたいです。"

    if CreateTweetVoteCommand.SPECIAL_CHARACTER_REGEX.match(text) is not None:
        log("command-create", "特殊な文字列が含まれています。")
        return "特殊な文字列が含まれています:thinking:\n" \
               "メンションやこの鯖独自の絵文字(<:ahe:724540322322972723>とか)はツイートできません。使えたら面白いんだけどな〜"

    return ""


def get_apparently_length(text: str) -> int:
    """
    文字列の見かけ上の長さを取得する。
    :param text: 文字列。
    :return: 見かけ上の長さ。
    """
    length = 0
    for c in text:
        width_text = unicodedata.east_asian_width(c)
        length += 2 if width_text in ["F", "W", "A"] else 1

    return length