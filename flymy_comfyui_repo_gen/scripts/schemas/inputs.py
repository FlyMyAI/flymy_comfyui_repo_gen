import enum


class YesOrNo(enum.StrEnum):
    YES = "y"
    NO = "n"

    def __bool__(self):
        return self == self.__class__.YES
