"""
reaction_event.py
------------------------
リアクションに変化があったときの処理が入っている。
"""
import discord

from lib.data.tweet_votes_record import TweetsVoteRecord
from lib.logging.logger import log
from lib.settings.setting import Setting


async def on_reaction_add(reaction: discord.Reaction, user: discord.Member, setting: Setting) -> bool:
    """
    リアクションが追加されたときに実行する処理。
    MainClientに書きたくなかったので分けた。
    :param reaction: リアクションが追加された対象のメッセージの、現在のリアクションの状態
    :param user: 誰「が」リアクションを追加したか (who)
    :param setting: Botの設定。
    :return: このイベントで可決が確定したか。
    """

    if user.bot:
        # Botがリアクションを追加した(原則的には初期化の時)は無視
        return False

    log("react-add", "{}がリアクションを追加しました。".format(user.name))

    # リアクションが適切なものであるかを確認する
    if validate_reaction(reaction, user, setting):
        # 不適切だった場合は削除する
        await reaction.message.remove_reaction(reaction.emoji, user)
        return False

    # TweetsVoteRecordから該当するTweetVoteを持ってくる
    tweet_vote = TweetsVoteRecord().get(reaction.message.id)

    # リアクションを基に投票状態を更新
    if reaction.emoji.id == setting.emoji_ids["approve"]:
        tweet_vote.approves += 1
    if reaction.emoji.id == setting.emoji_ids["deny"]:
        tweet_vote.denys += 1

    # 更新した情報をEmbedに反映する
    embed = tweet_vote.to_embed()
    embed.set_footer(text="ID: {}".format(reaction.message.id))
    await reaction.message.edit(embed=embed)

    # 可決状態になったかを返す
    return (
            (tweet_vote.approves + tweet_vote.denys) >= setting.approve_total and
            tweet_vote.approves / (tweet_vote.approves + tweet_vote.denys) * 100 >= setting.approve_rate
    )


async def on_reaction_remove(reaction: discord.Reaction, user: discord.Member, setting: Setting):
    """
    リアクションが削除されたときの処理。
    :param reaction: リアクションが削除された対象のメッセージの、現在のリアクションの状態
    :param user: 誰「の」リアクションが削除されたか (whose)
    :param setting: Botの設定。
    """

    # 参政権を持っていない人がリアクションを消しやがった
    if setting.suffrage_role_id not in [x.id for x in user.roles]:
        # お気持ち表明して帰る
        await reaction.message.channel.send(
            "お前！！！！！！！！！！！！！！！！なんてことしてくれたんだ！！！！！！！！！！！！！！！！！！！！！！\n"
            "***†卍 メス堕ち女装土下座生配信 卍†***奉れ！！！！！！！！！！！！！！！！よ！！！！！！！！！！！！！！！！！！！")
        return

    log("react-del", "{}がしたリアクションが削除されました。".format(user.name))

    # TweetsVoteRecordから該当するTweetVoteを持ってくる
    tweet_vote = TweetsVoteRecord().get(reaction.message.id)

    # リアクションを基に投票状態を更新する
    if reaction.emoji.id == setting.emoji_ids["approve"]:
        tweet_vote.approves -= 1
    if reaction.emoji.id == setting.emoji_ids["deny"]:
        tweet_vote.denys -= 1

    # Embedに反映する
    embed = tweet_vote.to_embed()
    embed.set_footer(text="ID: {}".format(reaction.message.id))
    await reaction.message.edit(embed=embed)


async def on_reaction_clear(message: discord.Message):
    """
    リアクションが全削除されたときに呼ばれる
    :param message: 該当するメッセージ
    """

    # お気持ち表明
    await message.channel.send(
        "お前？！？！！？？！？？！？？！？！？！？！おい！？？！？！？！？！？！？！？？！！？！？！？\n"
        "いっぱい消すな！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！\n"
        "今すぐツイッターでメス堕ちしろ！！！！！！！！！！！！！！！おい！！！！！！！！！！！！！！！！！！！！！！！！！"
    )

    log("react-clr", "ID: {}に関連付けされた投票が全て削除されました。該当する投票を登録から削除します。")

    # 整合性がvoidに還ったので消す
    TweetsVoteRecord().delete(message.id)
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

    # そのリアクションが投票を受け付けているかを確認する
    if TweetsVoteRecord().get(reaction.message.id) is None:
        log("reaction", "不正なメッセージへのリアクションでした。ロールバックが必要です。")
        return True

    # そのリアクションが適切な絵文字かを確認する
    if reaction.emoji.id not in setting.emoji_ids.values():
        log("reaction", "不正なリアクションです。ロールバックが必要です。")
        return True

    # そのリアクションをした人が参政権を持っているかを確認する
    if setting.suffrage_role_id not in [x.id for x in user.roles]:
        log("reaction", "不正なユーザーからのリアクションです。ロールバックが必要です。")
        return True

    # 何も問題なければロールバックは不要
    return False
