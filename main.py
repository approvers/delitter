"""
main.py
------------------------
プログラムのエントリポイント。
"""
from lib.data.tweet_votes_record import TweetsVoteRecord
from lib.discord.client import MainClient
from lib.discord.op.command.command_register import CommandRegister
from lib.discord.op.command.impl.create_vote_command import CreateVoteCommand
from lib.discord.op.command.impl.delete_vote_command import DeleteVoteCommand
from lib.discord.op.event.approve_discord_handler import ApproveDiscordHandler
from lib.discord.op.event.reaction_event import ReactionEvent
from lib.settings.discord_setting import DiscordSetting, create_discord_setting_from_json
from lib.settings.twitter_setting import TwitterSetting, create_twitter_setting_from_json

if __name__ == '__main__':
    with open("settings/discord.json", mode="r") as f:
        discord_setting: DiscordSetting = create_discord_setting_from_json(f)

    with open("settings/twitter-api.json", mode="r") as f:
        twitter_setting: TwitterSetting = create_twitter_setting_from_json(f)

    votes_record = TweetsVoteRecord()
    command_register = CommandRegister(discord_setting)

    command_register.add_command(CreateVoteCommand)
    command_register.add_command(DeleteVoteCommand)

    reaction_event_handler = ReactionEvent(discord_setting, votes_record)
    approve_event_handlers = [
        ApproveDiscordHandler()
    ]

    client = MainClient(discord_setting, votes_record, command_register, reaction_event_handler, approve_event_handlers)
    client.launch()
