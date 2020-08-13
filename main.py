"""
main.py
------------------------
プログラムのエントリポイント。
"""
import base64
import os

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

    if "DELITTER_DISCORD_SETTING_JSON_B64" not in os.environ:
        raise RuntimeError("DELITTER_DISCORD_SETTING_JSON_B64 is not set!")

    if "DELITTER_TWITTER_SETTING_JSON_B64" not in os.environ:
        raise RuntimeError("DELITTER_TWITTER_SETTING_JSON_B64 is not set!")

    raw_discord_setting = base64.b64decode(os.environ["DELITTER_DISCORD_SETTING_JSON_B64"]).decode("utf-8")
    raw_twitter_setting = base64.b64decode(os.environ["DELITTER_TWITTER_SETTING_JSON_B64"]).decode("utf-8")

    discord_setting: discord.DiscordSetting = discord.create(raw_discord_setting)
    twitter_setting: twitter.TwitterSetting = twitter.create(raw_twitter_setting)

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
