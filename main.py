"""
main.py
------------------------
プログラムのエントリポイント。
"""
from lib.discord.client import *
from lib.discord.op.command.impl.create_vote_command import CreateVoteCommand
from lib.discord.op.command.impl.delete_vote_command import DeleteVoteCommand
from lib.settings.setting import create_setting_from_json

if __name__ == '__main__':
    with open("./settings/settings.json", mode="r") as f:
        setting: Setting = create_setting_from_json(f)

    votes_record = TweetsVoteRecord()
    command_register = CommandRegister(setting)

    command_register.add_command(CreateVoteCommand)
    command_register.add_command(DeleteVoteCommand)

    client = MainClient(setting, votes_record, command_register)
    client.launch()
