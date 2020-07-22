from lib.discord.Client import *

if __name__ == '__main__':
    with open("./settings/settings.json", mode="r") as f:
        setting: MainClientSetting = MainClientSetting.load_from_json(f)

    MainClient(setting).launch()
