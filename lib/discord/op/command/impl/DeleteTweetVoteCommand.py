from abc import ABC

import discord

from lib.data.TweetsVoteRecord import TweetsVoteRecord
from lib.discord.op.command.ABCCommand import ABCCommand
from lib.discord.op.command.CommandInfo import CommandInfo
from lib.settings.Setting import Setting


class DeleteTweetVoteCommand(ABCCommand, ABC):
    """
    投票を削除するためのコマンド。
    """

    def __init__(self, guild: discord.Guild, setting: Setting):
        super().__init__(guild, setting)

    def get_command_info(self) -> CommandInfo:
        return CommandInfo(
            identify="del",
            args_format="(削除する投票のID)",
            name="投票を削除する",
            description="投票を削除します。投票を立てた人しか使えない安心安全の設計となっております。"
        )

    async def parse_command(self, text: str, message: discord.Message):

        # 投票IDを取得する
        try:
            tweet_id = int(text)
        except ValueError:
            # 数値じゃないやん！どうしてくれんのこれ！
            await message.channel.send("なんだお前IDは数値で入力してクレメンス")
            return

        # 該当する投票があるか
        if TweetsVoteRecord().get(tweet_id) is None:
            await message.channel.send("残念、IDが間違っています")
            return

        # 該当する投票を削除する
        TweetsVoteRecord().delete(tweet_id)
        await (await message.channel.fetch_message(tweet_id)).delete()

        await message.channel.send("ID`{}` の投票を削除しました。".format(tweet_id))

