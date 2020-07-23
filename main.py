"""
main.py
------------------------
プログラムのエントリポイント。
"""

from lib.discord.client import *
from lib.discord.op.command.impl.create_vote_command import CreateVoteCommand
from lib.discord.op.command.impl.delete_vote_command import DeleteVoteCommand

if __name__ == '__main__':
    with open("./settings/settings.json", mode="r") as f:
        setting: Setting = Setting.load_from_json(f)

    client = MainClient(setting)
    client.add_command(CreateVoteCommand)
    client.add_command(DeleteVoteCommand)
    client.launch()
