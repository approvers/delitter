class JudgeStandard:

    def __init__(self, required_total, required_rate):
        self.__required_total = required_total
        self.__required_rate = required_rate

    @property
    def required_total(self):
        return self.__required_total

    @property
    def required_rate(self):
        return self.__required_rate
