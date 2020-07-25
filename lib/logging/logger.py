"""
logger.py
------------------------
標準出力にログを取るための関数が入っている。
"""
from datetime import datetime


def log(tag: str, msg: str):
    """
    ログを出力する。
    :param tag: ログの種類。
    :param msg: ログの内容。
    """
    print(
        "[{}] \"{}\": {}".format(
            datetime.now().strftime("%m-%d %H:%M:%S.%f"),
            tag,
            msg
        )
    )
