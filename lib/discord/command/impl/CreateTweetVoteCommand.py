from abc import ABC

import discord

from lib.discord import Client
from lib.discord.command.ABCCommand import ABCCommand
from lib.discord.command.CommandInfo import CommandInfo
from lib.logging.Logger import log


class CreateTweetVoteCommand(ABCCommand, ABC):

    def get_command_info(self) -> CommandInfo:
        return CommandInfo(
           identify="create",
           args_format="(ツイートの内容)",
           name="ツイートを作成する",
           description="ツイートしたい内容を"
        )

    async def parse_command(self, text: str, author: discord.User, client: Client):
        log("command-create", "ツイートの作成コマンドを受信しました。")
        await client.activity_channel.send("`NotImplementedException`")
