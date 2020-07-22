import re
import unicodedata
from abc import ABC
from math import ceil

import discord

from lib.discord.command.ABCCommand import ABCCommand
from lib.discord.command.CommandInfo import CommandInfo
from lib.logging.Logger import log


class CreateTweetVoteCommand(ABCCommand, ABC):
    SPECIAL_CHARACTER_REGEX: re.Pattern = re.compile("<[@#:].*?>")

    def get_command_info(self) -> CommandInfo:
        return CommandInfo(
            identify="create",
            args_format="(ツイートの内容)",
            name="ツイートを作成する",
            description="ツイートしたい内容を"
        )

    async def parse_command(self, text: str, message: discord.Message):
        log("command-create", "ツイートの作成コマンドを受信しました。")

        apparent_len = get_apparently_length(text)
        if apparent_len > 240:
            log("command-create", "文字列が長すぎました。({} > 240)".format(apparent_len))
            await message.channel.send(
                "テキストが長すぎるみたいです:thinking:\n"
                "{}文字あって{}文字オーバーしてるので削ってみてください。"
                .format(ceil(apparent_len / 2), ceil(apparent_len / 2 - 240))
            )
            return

        if CreateTweetVoteCommand.SPECIAL_CHARACTER_REGEX.match(text) is not None:
            log("command-create", "特殊な文字列が含まれています。")
            await message.channel.send(
                "特殊な文字列が含まれています:thinking:\n"
                "メンションやこの鯖独自の絵文字(<:ahe:724540322322972723>とか)はツイートできません。使えたら面白いんだけどな〜"
            )
            return

        log("command-create", "問題ありませんでした。")
        await message.channel.send("Passed:```{}```".format(text))


def get_apparently_length(text: str) -> int:
    length = 0
    for c in text:
        width_text = unicodedata.east_asian_width(c)
        length += 2 if width_text in ["F", "W", "A"] else 1

    return length
