class JudgeStandard:

    def __init__(self, required_total, required_rate):
        self.__required_total = required_total
        self.__required_rate = required_rate

    @property
    def required_total(self):
        pass

    @property
    def required_rate(self):
        pass

    @required_total.getter
    def required_total(self) -> int:
        return self.__required_total

    @required_rate.getter
    def required_rate(self) -> int:
        return self.__required_rate
