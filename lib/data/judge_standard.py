"""
judge_standard.py
------------------------
可決の基準を表すクラスが入っている。
"""


class JudgeStandard:
    """
    可決する基準となる情報を格納するクラス。
    """

    def __init__(self, required_total, required_rate):
        """
        JudgeStandardを初期化する。
        :param required_total: 可決に必要な総票数。
        :param required_rate: 可決に必要な可決率。
        """
        self.__required_total = required_total
        self.__required_rate = required_rate

    @property
    def required_total(self):
        return self.__required_total

    @property
    def required_rate(self):
        return self.__required_rate
