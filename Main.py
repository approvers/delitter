from lib.discord.Client import *
from lib.discord.command.impl.CreateTweetVoteCommand import CreateTweetVoteCommand
from lib.discord.command.impl.DeleteTweetVoteCommand import DeleteTweetVoteCommand

if __name__ == '__main__':
    with open("./settings/settings.json", mode="r") as f:
        setting: Setting = Setting.load_from_json(f)

    client = MainClient(setting)
    client.add_command(CreateTweetVoteCommand)
    client.add_command(DeleteTweetVoteCommand)
    client.launch()
