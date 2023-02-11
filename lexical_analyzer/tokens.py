from typing import Optional, Any

#  main function
RETURN = "RETURN"
RETURN_V = "return"

MAIN = "MAIN"
MAIN_V = "main()"


#  system names
INCLUDE = "INCLUDE"
INCLUDE_V = "include"

NAMESPACE = "NAMESPACE"
NAMESPACE_V = "namespace"

USING = "USING"
USING_V = "using"

EOF = "EOF"


#  system symbols
SHARP = "SHARP"
SHARP_V = "#"

LARROW = "LARROW"
LARROW_V = "<"

RARROW = "RARROW"
RARROW_V = ">"

SEMI = "SEMI"
SEMI_V = ";"

SINGLE_QUOTE = "SINGLE_QUOTE"
SINGLE_QUOTE_V = "'"

DOUBLE_QUOTE = "DOUBLE_QUOTE"
DOUBLE_QUOTE_V = "\""

FORWARD_SLASH = "FORWARD_SLASH"
FORWARD_SLASH_V = "/"

BACK_SLASH = "BACK_SLASH"
BACK_SLASH_V = "\\"

COMMENT = "COMMENT"
COMMENT_V = "//"

COLON = "COLON"
COLON_V = ":"

COMMA = "COMMA"
COMMA_V = ","


#  expression symbols
ASSIGN = "ASSIGN"
ASSIGN_V = "="

PLUS = "PLUS"
PLUS_V = "+"

MINUS = "MINUS"
MINUS_V = "-"

ASTERISK = "ASTERISK"
ASTERISK_V = "*"

DOT = "DOT"
DOT_V = "."


#  data types
INTEGER = "INTEGER"
INTEGER_V = "int"

FLOAT = "FLOAT"
FLOAT_V = "float"

DOUBLE = "DOUBLE"
DOUBLE_V = "double"

CHAR = "CHAR"
CHAR_V = "char"

CONST = "CONST"
CONST_V = "const"


#  consts
INTEGER_CONST = "INTEGER_CONST"
FLOAT_CONST = "FLOAT_CONST"
DOUBLE_CONST = "DOUBLE_CONST"
CHAR_SINGLE_CONST = "CHAR_SINGLE_CONST"
CHAR_MULTI_CONST = "CHAR_MULTI_CONST"


#  comparison
LESS_THEN_EQ = "LESS_THEN_EQ"
LESS_THEN_EQ_V = "<="

GREATER_THEN_EQ = "GREATER_THEN_EQ"
GREATER_THEN_EQ_V = ">="

EQUAL = "EQUAL"
EQUAL_V = "=="

NOT_EQUAL = "NOT_EQUAL"
NOT_EQUAL_V = "!="

LOGICAL_END = "LOGICAL_END"
LOGICAL_END_V = "&&"

LOGICAL_OR = "LOGICAL_OR"
LOGICAL_OR_V = "||"

LOGICAL_NOT = "LOGICAL_NOT"
LOGICAL_NOT_V = "!"


#  id
ID = "ID"


#  braces
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

    @property
    def type(self):
        return self.__type

    def __str__(self):
        return f"Token ({self.__type}, {self.__value})"

    def __repr__(self):
        return self.__str__()


#  Reserved keywords
RESERVED_KEYWORDS = {
    INTEGER_V: Token(INTEGER, INTEGER_V),
    FLOAT_V: Token(FLOAT, FLOAT_V),
    RETURN_V: Token(RETURN, RETURN_V),
    INCLUDE_V: Token(INCLUDE, INCLUDE_V),
    MAIN_V: Token(MAIN, MAIN_V),
    USING_V: Token(USING, USING_V),
}
