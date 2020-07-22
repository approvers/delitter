import discord

from lib.data.PendingTweetsManager import PendingTweetsManager
from lib.discord.Setting import Setting
from lib.logging.Logger import log


async def on_reaction_add(reaction: discord.Reaction, user: discord.Member, setting: Setting):

    if validate_reaction(reaction, user, setting):
        await reaction.message.remove_reaction(reaction.emoji, user)
        return

    manager = PendingTweetsManager()
    tweet_vote = manager.get(reaction.message.id)

    if reaction.emoji.id == setting.emoji_ids["approve"]:
        tweet_vote.approves += 1
    if reaction.emoji.id == setting.emoji_ids["deny"]:
        tweet_vote.denys += 1

    await reaction.message.edit(embed=tweet_vote.to_embed())


def validate_reaction(reaction: discord.Reaction, user: discord.Member, setting: Setting):
    """
    リアクションが適切か確認し、ロールバックが必要かを判断する。
    :param reaction: バリデートするリアクション。
    :param user: リアクションしたユーザー。
    :param setting: 設定情報。
    :return: ロールバックが必要な場合はTrue、必要ない場合はFalse。
    """
    manager = PendingTweetsManager()
    if manager.get(reaction.message.id) is None:
        log("reaction", "不正なメッセージへのリアクションでした。ロールバックが必要です。")
        return True

    if reaction.emoji.id not in setting.emoji_ids.values():
        log("reaction", "不正なリアクションです。ロールバックが必要です。")
        return True

    if setting.suffrage_role_id not in [x.id for x in user.roles]:
        log("reaction", "不正なユーザーからのリアクションです。ロールバックが必要です。")
        return True

    return False

