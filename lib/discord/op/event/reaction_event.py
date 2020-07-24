"""
reaction_event.py
------------------------
リアクションに変化があったときの処理が入っている。
"""

import discord

from lib.data.tweet_votes_record import TweetsVoteRecord
from lib.discord.tweet_vote_utils import create_tweet_vote_embed
from lib.logging.logger import log
from lib.settings.setting import Setting


class ReactionEvent:

    RESPOND_REQUIRED = 0
    NO_RESPOND_REQUIRED = 1
    ROLLBACK_REQUIRED = 2

    def __init__(self, setting: Setting, vote_record: TweetsVoteRecord):
        """
        ReactionEventを初期化する。
        :param setting: Botの設定。
        :param vote_record: ツイートの投票が記録されたレコード。
        """
        self.setting = setting
        self.vote_record = vote_record

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member) -> bool:
        """
        リアクションが追加されたときに実行する処理。
        MainClientに書きたくなかったので分けた。
        :param reaction: リアクションが追加された対象のメッセージの、現在のリアクションの状態
        :param user: 誰「が」リアクションを追加したか (who)
        :return: このイベントで可決が確定したか。
        """

        # イベントに対してどう反応すべきかを確認する
        response = self.validate_reaction(reaction, user)

        # 反応の必要がないか
        if response == ReactionEvent.NO_RESPOND_REQUIRED:
            return False

        # ロールバックが必要か
        if response == ReactionEvent.ROLLBACK_REQUIRED:
            await reaction.message.remove_reaction(reaction.emoji, user)
            return False

        # TweetsVoteRecordから該当するTweetVoteを持ってくる
        tweet_vote = self.vote_record.get(reaction.message.id)

        # リアクションを基に投票状態を更新
        if reaction.emoji.id == self.setting.emoji_ids["approve"]:
            tweet_vote.approves += 1
        if reaction.emoji.id == self.setting.emoji_ids["deny"]:
            tweet_vote.denys += 1

        # 反映する
        self.vote_record.set(reaction.message.id, tweet_vote)

        # 更新した情報をEmbedに反映する
        embed = create_tweet_vote_embed(tweet_vote)
        embed.set_footer(text="ID: †{}†".format(reaction.message.id))
        await reaction.message.edit(embed=embed)

        return tweet_vote.is_approved(self.setting.judge_standard)

    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.Member):
        """
        リアクションが削除されたときの処理。
        :param reaction: リアクションが削除された対象のメッセージの、現在のリアクションの状態
        :param user: 誰「の」リアクションが削除されたか (whose)
        """

        # イベントに対してどう反応すべきかを確認する
        response = self.validate_reaction(reaction, user)

        # 反応の必要がないか
        if response == ReactionEvent.NO_RESPOND_REQUIRED:
            return False

        # ロールバックが必要か
        if response == ReactionEvent.ROLLBACK_REQUIRED:
            # 削除されるとロールバックでないのでお気持ち表明して帰る
            await reaction.message.channel.send(
                "お前！！！！！！！！！！！！！！！！なんてことしてくれたんだ！！！！！！！！！！！！！！！！！！！！！！\n"
                "***†卍 メス堕ち女装土下座生配信 卍†***奉れ！！！！！！！！！！！！！！！！よ！！！！！！！！！！！！！！！！！！！")
            return

        log("react-del", "{}がしたリアクションが削除されました。".format(user.name))

        # TweetsVoteRecordから該当するTweetVoteを持ってくる
        tweet_vote = self.vote_record.get(reaction.message.id)

        # リアクションを基に投票状態を更新する
        if reaction.emoji.id == self.setting.emoji_ids["approve"]:
            tweet_vote.approves -= 1
        if reaction.emoji.id == self.setting.emoji_ids["deny"]:
            tweet_vote.denys -= 1

        # 反映する
        self.vote_record.set(reaction.message.id, tweet_vote)

        # Embedに反映する
        embed = create_tweet_vote_embed(tweet_vote)
        embed.set_footer(text="ID: †{}†".format(reaction.message.id))
        await reaction.message.edit(embed=embed)

    async def on_reaction_clear(self, message: discord.Message):
        """
        リアクションが全削除されたときに呼ばれる
        :param message: 該当するメッセージ
        """

        if self.vote_record.get(message.id) is None:
            return

        # お気持ち表明
        await message.channel.send(
            "お前？！？！！？？！？？！？？！？！？！？！おい！？？！？！？！？！？！？！？？！！？！？！？\n"
            "いっぱい消すな！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！\n"
            "今すぐツイッターでメス堕ちしろ！！！！！！！！！！！！！！！おい！！！！！！！！！！！！！！！！！！！！！！！！！"
        )

        log("react-clr", "ID: {}に関連付けされた投票が全て削除されました。該当する投票を登録から削除します。".format(message.id))

        # 整合性がvoidに還ったので消す
        self.vote_record.delete(message.id)
        embed: discord.Embed = message.embeds[0]
        embed.title = "†無効投票 (リアクションぶっち)†"

        await message.edit(content="この投票は無効投票になりました。", embed=embed)
        await message.channel.send("投票が全てぶっちされたので、無効投票になってしまいました。お前のせいです。あーあ")

    def validate_reaction(self, reaction: discord.Reaction, user: discord.Member) -> int:
        """
        リアクションが適切か確認し、ロールバックが必要かを判断する。
        :param reaction: バリデートするリアクション。
        :param user: リアクションしたユーザー。
        :return: ロールバックが必要な場合はTrue、必要ない場合はFalse。
        """

        if self.vote_record.get(reaction.message.id) is None:
            return ReactionEvent.NO_RESPOND_REQUIRED

        # そのリアクションが適切な絵文字かを確認する
        if reaction.emoji.id not in self.setting.emoji_ids.values():
            log("reaction", "不正なリアクションです。")
            return ReactionEvent.NO_RESPOND_REQUIRED

        # そのリアクションをした人が参政権を持っているかを確認する
        if self.setting.suffrage_role_id not in [x.id for x in user.roles]:
            log("reaction", "不正なユーザーからのリアクションです。ロールバックが必要です。")
            return ReactionEvent.ROLLBACK_REQUIRED

        # 何も問題なければロールバックは不要
        return ReactionEvent.RESPOND_REQUIRED

