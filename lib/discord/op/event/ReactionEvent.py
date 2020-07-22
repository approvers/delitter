import discord

from lib.data.PendingTweetsManager import PendingTweetsManager
from lib.discord.Setting import Setting
from lib.logging.Logger import log


async def on_reaction_add(reaction: discord.Reaction, user: discord.Member, setting: Setting):

    manager = PendingTweetsManager()
    if manager.get(reaction.message.id) is None:
        log("reaction", "不正なメッセージへのリアクションでした。無視します。")
        return

    emoji: discord.Emoji = reaction.emoji
    if emoji.id not in setting.emoji_ids.values():
        log("reaction", "不正なリアクションです。削除します。")
        message: discord.Message = reaction.message
        await message.remove_reaction(emoji, user)
        return

    if setting.suffrage_role_id not in [x.id for x in user.roles]:
        log("reaction", "不正なユーザーからのリアクションです。削除します。")
        await reaction.message.remove_reaction(emoji, user)
        return

    tweet_vote = manager.get(reaction.message.id)

    if emoji.id == setting.emoji_ids["approve"]:
        tweet_vote.approves += 1
    if emoji.id == setting.emoji_ids["deny"]:
        tweet_vote.denys += 1

    await reaction.message.edit(embed=tweet_vote.to_embed())

