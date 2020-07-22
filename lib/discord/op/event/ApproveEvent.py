import discord

from lib.data.PendingTweetsManager import PendingTweetsManager
from lib.logging.Logger import log


async def on_approved(message: discord.Message):
    log("on_approved", "可決を確認しました。")

    new_embed = message.embeds[0]
    new_embed.title = "†可決†"
    await message.edit(content="この投票は可決されました！もう受け付けていません。", embed=new_embed)

    PendingTweetsManager().delete(message.id)
