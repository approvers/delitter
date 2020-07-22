from datetime import datetime


def log(tag: str, msg: str):
    print(
        "[{}] \"{}\": {}".format(
            datetime.now().strftime("%m-%d %H:%M:%S.%f"),
            tag,
            msg
        )
    )
