from typing import Optional, Any

###  main function  ###
INT,        INT_V =     "INT",      "int"
RETURN,     RETURN_V =  "RETURN",   "return"
MAIN,       MAIN_V =    "MAIN",     "main()"

###  system symbols  ###
SHARP =         "SHARP"
SHARP_V =         "#"

INCLUDE =       "INCLUDE"
INCLUDE_V =     "include"

LARROW =        "LARROW"
LARROW_V =      "<"

RARROW =        "RARROW"
RARROW_V =      ">"

SEMI =          "SEMI"
SEMI_V =        ";"

USING =         "USING"
USING_V =       "using"

NAMESPACE =     "NAMESPACE"
NAMESPACE_V =   "using"

STD =           "STD"
STD_V =         "std"


###  symbols  ###
SEMI = "SEMI"
SEMI_V = ";"

ASSIGN = "ASSIGN"
ASSIGN_V = "="

PLUS = "PLUS"
PLUS_V = "+"

MINUX = "MINUX"
MINUX_V = "-"


# data types
FLOAT = "FLOAT"
FLOAT_V = "float"

# braces
LBRACE = "LBRACE"
LBRACE_V = "{"

RBRACE = "RBRACE"
RBRACE_V = "}"

LPAREN = "LPAREN"
LPAREN_V = "("

RPAREN = "RPAREN"
RPAREN_V = ")"


class Token:
    """
    Represents token used for parsing input
    :type - type of the token
    :value - value of the token
    """
    def __init__(self, type: str, value: Optional[Any]):
        self.__type = type
        self.__value = value

    @property
    def value(self):
        return self.__value

    def 


###  Reserved keywords  ###
RESERVED_KEYWORDS = {
    INT_V: Token(INT, INT_V),
    RETURN_V: Token(RETURN, RETURN_V),
    INCLUDE_V: Token(INCLUDE, INCLUDE_V),
    MAIN_V: Token(MAIN, MAIN_V),
}