"""
These symbols will be simply parsed as tokens with corresponding content
"""

#  braces
LBRACKET = "LBRACKET"
LBRACKET_V = "{"

RBRACKET = "RBRACKET"
RBRACKET_V = "}"

LPAREN = "LPAREN"
LPAREN_V = "("

RPAREN = "RPAREN"
RPAREN_V = ")"


#  system symbols
HASH = "HASH"
HASH_V = "#"

SEMI = "SEMI"
SEMI_V = ";"

COLON = "COLON"
COLON_V = ":"

COMMA = "COMMA"
COMMA_V = ","

DOT = "DOT"
DOT_V = "."

BACK_SLASH = "BACK_SLASH"
BACK_SLASH_V = "\\"


#  expression symbols
ASSIGN = "ASSIGN"
ASSIGN_V = "="

PLUS = "PLUS"
PLUS_V = "+"

MINUS = "MINUS"
MINUS_V = "-"

ASTERIKS = "ASTERIKS"
ASTERIKS_V = "*"

DIVIDE = "DIVIDE"
DIVIDE_V = "/"

MOD = "MOD"
MOD_V = "%"

XOR_OP = "XOR_OP"
XOR_OP_V = "^"

INC_OP = "INC_OP"
INC_OP_V = "++"

DEC_OP = "DEC_OP"
DEC_OP_V = "--"

PLUS_ASSIGN = "PLUS_ASSIGN"
PLUS_ASSIGN_V = "+="

MINUS_ASSIGN = "MINUS_ASSIGN"
MINUS_ASSIGN_V = "-="

MUL_ASSIGN = "MUL_ASSIGN"
MUL_ASSIGN_V = "*="

DIVIDE_ASSIGN = "DIVIDE_ASSIGN"
DIVIDE_ASSIGN_V = "/="

MOD_ASSIGN = "MOD_ASSIGN"
MOD_ASSIGN_V = "%="

XOR_ASSIGN = "XOR_ASSIGN"
XOR_ASSIGN_V = "^="

RIGHT_OP = "RIGHT_OP"
RIGHT_OP_V = ">>"

LEFT_OP = "LEFT_OP"
LEFT_OP_V = "<<"

LOG_NOT = "LOG_NOT"
LOG_NOT_V = "!"

NOT_OP = "NOT_OP"
NOT_OP_V = "~"

AND_OP = "AND_OP"
AND_OP_V = "&"

OR_OP = "OR_OP"
OR_OP_V = "|"

QUESTION_MARK = "QUESTION_MARK"
QUESTION_MARK_V = "?"

COMMA = "COMMA"
COMMA_V = ","


#  comparison
LESS = "LESS"
LESS_V = "<"

GREATER = "GREATER"
GREATER_V = ">"

LE_OP = "LE_OP"
LE_OP_V = "<="

GE_OP = "GE_OP"
GE_OP_V = ">="

EQUAL = "EQUAL"
EQUAL_V = "=="

NOT_EQUAL = "NOT_EQUAL"
NOT_EQUAL_V = "!="

LOG_AND = "LOG_AND"
LOG_AND_V = "&&"

LOG_OR = "LOG_OR"
LOG_OR_V = "||"

