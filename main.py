"""
main.py
------------------------
プログラムのエントリポイント。
"""
from lib.discord.client import *
from lib.discord.op.command.impl.create_vote_command import CreateVoteCommand
from lib.discord.op.command.impl.delete_vote_command import DeleteVoteCommand
from lib.discord.op.event.approve_discord_handler import ApproveDiscordHandler
from lib.settings.discord_setting import create_setting_from_json

if __name__ == '__main__':
    with open("settings/discord.json", mode="r") as f:
        setting: DiscordSetting = create_setting_from_json(f)

    votes_record = TweetsVoteRecord()
    command_register = CommandRegister(setting)

    command_register.add_command(CreateVoteCommand)
    command_register.add_command(DeleteVoteCommand)

    reaction_event_handler = ReactionEvent(setting, votes_record)
    approve_event_handlers = [
        ApproveDiscordHandler()
    ]

    client = MainClient(setting, votes_record, command_register, reaction_event_handler, approve_event_handlers)
    client.launch()
