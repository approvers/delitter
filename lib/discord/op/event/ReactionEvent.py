import discord

from lib.data.PendingTweetsManager import PendingTweetsManager
from lib.logging.Logger import log
from lib.settings.Setting import Setting


async def on_reaction_add(reaction: discord.Reaction, user: discord.Member, setting: Setting):

    if user.bot:
        return

    log("react-add", "{}がリアクションを追加しました。".format(user.name))

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


async def on_reaction_remove(reaction: discord.Reaction, user: discord.Member, setting: Setting):

    if setting.suffrage_role_id not in [x.id for x in user.roles]:
        msg: discord.Message
        await reaction.message.channel.send(
            "お前！！！！！！！！！！！！！！！！なんてことしてくれたんだ！！！！！！！！！！！！！！！！！！！！！！\n"
            "***†卍 メス堕ち女装土下座生配信 卍†***奉れ！！！！！！！！！！！！！！！！よ！！！！！！！！！！！！！！！！！！１")
        return

    log("react-del", "{}がしたリアクションが削除されました。".format(user.name))
    tweet_vote = PendingTweetsManager().get(reaction.message.id)

    if reaction.emoji.id == setting.emoji_ids["approve"]:
        tweet_vote.approves -= 1
    if reaction.emoji.id == setting.emoji_ids["deny"]:
        tweet_vote.denys -= 1

    await reaction.message.edit(embed=tweet_vote.to_embed())


async def on_reaction_clear(message: discord.Message):
    await message.channel.send(
        "お前？！？！！？？！？？！？？！？！？！？！おい！？？！？！？！？！？！？！？？！！？！？！？\n"
        "いっぱい消すな！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！\n"
        "今すぐツイッターでメス堕ちしろ！！！！！！！！！！！！！！！おい！！！！！！！！！！！！！！！！！！！！！！！！！"
    )

    log("react-clr", "ID: {}に関連付けされた投票が全て削除されました。該当する投票を登録から削除します。")

    manager = PendingTweetsManager()
    manager.delete(message.id)
    await message.delete()

    await message.channel.send("投票が全てぶっちされたので、該当するメッセージを削除しました。号泣しています。")


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

