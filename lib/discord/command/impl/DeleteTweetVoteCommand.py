from abc import ABC

import discord

from lib.data.PendingTweetsManager import PendingTweetsManager
from lib.discord.Setting import Setting
from lib.discord.command.ABCCommand import ABCCommand
from lib.discord.command.CommandInfo import CommandInfo


class DeleteTweetVoteCommand(ABCCommand, ABC):

    def __init__(self, guild: discord.Guild, setting: Setting):
        super().__init__(guild, setting)
        self.tweet_manager = PendingTweetsManager()

    def get_command_info(self) -> CommandInfo:
        return CommandInfo(
            identify="del",
            args_format="(削除する投票のID)",
            name="投票を削除する",
            description="投票を削除します。投票を立てた人しか使えない安心安全の設計となっております。"
        )

    async def parse_command(self, text: str, message: discord.Message):
        try:
            tweet_id = int(text)
        except ValueError:
            await message.channel.send("なんだお前IDは数値で入力してクレメンス")
            return

        if self.tweet_manager.get(tweet_id) is None:
            await message.channel.send("残念、IDが間違っています")
            return

        self.tweet_manager.delete(tweet_id)
        await (await message.channel.fetch_message(tweet_id)).delete()

        await message.channel.send("ID`{}` の投票を削除しました。".format(tweet_id))

