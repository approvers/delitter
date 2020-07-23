"""
approve_event.py
------------------------
投票が可決されたときに発火される関数が入っている。
"""
import discord

from lib.data.tweet_votes_record import TweetsVoteRecord
from lib.logging.logger import log


async def on_approved(message: discord.Message):
    """
    リアクションが可決されたときに発火されるイベント。
    Discord周りを処理する。
    :param message: 該当するメッセージ。
    """
    log("on_approved", "可決を確認しました。")

    new_embed = message.embeds[0]
    new_embed.title = "†可決†"
    await message.edit(content="この投票は可決されました！もう受け付けていません。", embed=new_embed)

    TweetsVoteRecord.delete(message.id)
