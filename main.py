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
from lib.discord.op.event.approve_twitter_handler import ApproveTwitterHandler
from lib.discord.op.event.reaction_event import ReactionEvent
from lib.settings import twitter, discord
from lib.twitter.tweeter import Tweeter

if __name__ == '__main__':
    with open("settings/discord.json") as f:
        discord_setting: discord.DiscordSetting = discord.create(f)

    with open("settings/twitter-api.json") as f:
        twitter_setting: twitter.TwitterSetting = twitter.create(f)

    votes_record = TweetsVoteRecord()
    command_register = CommandRegister(discord_setting)

    command_register.add_command(CreateVoteCommand)
    command_register.add_command(DeleteVoteCommand)

    reaction_event_handler = ReactionEvent(discord_setting, votes_record)
    approve_event_handlers = [
        ApproveTwitterHandler(Tweeter(twitter_setting)),
        ApproveDiscordHandler()
    ]

    client = MainClient(discord_setting, votes_record, command_register, reaction_event_handler, approve_event_handlers)
    client.launch()
