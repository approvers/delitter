# delitter

IDEAでmarkdown編集すると日本語が文字化けしちゃうのなんで？

## 概要

Dagger_TweetManagementSystem_Daggerが止まってしまったので開発してみようかなになったので立てました。

### したいこと

**ツイートしたいことをコマンドから登録し、投票の結果問題なければ自動ツイートする。**

## やること

1. 指定のチャンネルでコマンドを叩いてもらう
2. Botが投票を促す
   1. 情報が適切化をバリデーションする
   2. Bot内部の配列に登録する[^1]
   3. 投票用のメッセージを作成し、管理する
   4. リアクションをつける(可決用と否決用一つずつ)
3. 投票してもらう
   1. リアクションが来たことを確認する
   2. 適切なリアクションでなければ外す（余計なのは紛らわしいので外しちゃいます）
   3. 参政権を持っていない人だったら…
      1. お気持ち表明メッセージを送信する
      2. リアクションを外す
   4. 投票を登録する
4. ツイートの可否に応じてツイートする／否決する
   1. 可決票が一定数貯まる and 可決率が一定数以上になるまで待機
   2. ツイートする
   3. 監視を終了する

[^1]: Firebaseとかにしようと思ったんですが、そんな再起動しない(Herokuで動かします)し消えても死ぬほど困るわけでもないのでいいかなのお気持ちになりました（まずかったら***Inform***してください）

### これからの予定

動的にすると大変になるので書いておきます。
`等幅フォント`のところはブランチ名(予定)です。各ブランチごとのTodoは~~(忘れなければ)~~DraftのPRで管理します。

- [ ] `bot-base`: Botでツイートの可否を問うことができる。
  - [ ] `client`: サーバーに挨拶をすることができる。
  - [ ] `acquire-info`: ユーザーから**適切な**情報を取得することができる。
  - [ ] `info-management`: ユーザーから得た情報を管理することができる。
  - [ ] `reaction`: リアクションを用いて可否を確認することができる。
  - [ ] `final-judge`: ツイートをするかどうかの最終判断ができる。
  - [ ] `connect-firebase`:  ユーザーから得た情報をFirebase上で管理することができる。
- [ ] `tweet-base`: Twitterにツイートすることができる。[^2]
  - [ ] `twitter-api`: 任意のツイートをすることができる。
  - [ ] `tweet`: 可決されたツイートを送信することができる。
  - [ ] `connect-firebase`: ツイート後にFirebaseから情報を削除することができる。

[^2]: マジで何も分からんので誰かに投げるかもしれません…
