"""
delete_vote_command.py
------------------------
投票を削除するためのコマンドが入っている。
"""
from abc import ABC

import discord

from lib.data.tweet_votes_record import TweetsVoteRecord
from lib.discord.op.command.abst_command_base import AbstCommandBase
from lib.discord.op.command.command_property import CommandProperty
from lib.settings.discord_setting import DiscordSetting


class DeleteVoteCommand(AbstCommandBase, ABC):
    """
    投票を削除するためのコマンド。
    """

    def __init__(self, guild: discord.Guild, setting: DiscordSetting, vote_record: TweetsVoteRecord):
        super().__init__(guild, setting, vote_record)
        self.vote_record = vote_record

    def get_command_info(self) -> CommandProperty:
        return CommandProperty(
            identify="del",
            args_format="(削除する投票のID)",
            name="投票を削除する",
            description="投票を削除します。投票を立てた人しか使えない安心安全の設計となっております。"
        )

    async def execute_command(self, text: str, message: discord.Message):

        # 投票IDを取得する
        try:
            tweet_id = int(text)
        except ValueError:
            # 数値じゃないやん！どうしてくれんのこれ！
            await message.channel.send("なんだお前IDは数値で入力してクレメンス")
            return

        record = self.vote_record.get(tweet_id)
        # 該当する投票があるか
        if record is None:
            await message.channel.send("残念、IDが間違っています")
            return

        # 投票が削除しようとしている人によって作成されたものかどうかを確認する
        if record.author_id != message.author.id:
            await message.channel.send("人の投票消さないで♥")
            return

        # 該当する投票を無効投票にする
        self.vote_record.delete(tweet_id)
        vote_message: discord.Message = await message.channel.fetch_message(tweet_id)
        embed: discord.Embed = vote_message.embeds[0]
        embed.title = "†無効投票 (削除)†"

        await vote_message.edit(content="この投票は無効投票になりました。", embed=embed)
        await message.channel.send("ID †`{}`† の投票は無効投票になりました。".format(tweet_id))
