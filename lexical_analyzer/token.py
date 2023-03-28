from typing import Optional, Any


class Token:
    """
    Represents token used for parsing input
    Output from Lexical analysis is list of tokens
    :type - type of the token
    :value - value of the token
    """
    def __init__(self, type: str, value: Optional[Any]):
        self.__type = type
        self.__value = value

    @property
    def value(self):
        return self.__value

    @property
    def type(self):
        return self.__type

    def __str__(self):
        """String representation of the token
        Examples:
                Token(INTEGER, 3)
                Token(PLUS, '+')
                Token(ASTERIKS, '*')
        """
        return f"Token ({self.__type}, {self.__value})"

    def __repr__(self):
        return self.__str__()

