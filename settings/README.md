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
  "approve_rate": (可決に必要な、参政権を持っている人に対する可決票の割合)
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