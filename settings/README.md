# delitter/setings
ここに以下の書式で設定ファイル「`discord.json`」と「`twitter-api.json`」を設置する必要があります。

## `discord.json`
```json
{
  "activity_channel_id": (このBotが活動するチャンネルID),
  "token": "Discordのトークン(なくても可、ない場合はDISCORD_TOKEN環境変数から読み込む)",
  "prefix": "Botのプレフィックス。",
  "emoji_ids": {
    "approve": "可決票の絵文字ID",
    "deny": "否決表の絵文字ID"
  },
  "suffrage_role_id": (参政権のロールID),
  "judge_standard": {
    "total": (可決に必要な総票数),
    "rate": (可決に必要な可決率)
  }
}
```

## `twitter-api.json`
```json
{
  "consumer_api_key": "Consumer Api Key",
  "consumer_api_secret_key": "Consumer Api Secret Key",
  "access_token": "Access Token",
  "access_token_secret": "Access Token Secret"            
}
```