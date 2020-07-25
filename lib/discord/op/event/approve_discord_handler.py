"""
approve_discord_handler.py
------------------------
可決されたときのDiscord周りの処理を司る。
"""
from abc import ABC

import discord

from lib.data.tweet_votes_record import TweetsVoteRecord
from lib.discord.op.event.approve_event import ApproveEvent
from lib.logging.logger import log


class ApproveDiscordHandler(ApproveEvent, ABC):
    """
    投票が可決されたときのDiscordの処理を実施する。
    """

    async def on_approved(self, message: discord.Message, vote_record: TweetsVoteRecord):
        log("on_approved", "可決を確認しました。")

        new_embed = message.embeds[0]
        new_embed.title = "†可決†"
        await message.edit(content="この投票は可決されました！", embed=new_embed)

        vote_record.delete(message.id)
