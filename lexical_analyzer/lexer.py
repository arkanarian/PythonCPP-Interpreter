from typing import Any, Union
import os

import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(path))

from lexical_analyzer.token import Token
from lexical_analyzer.token_types import *
import lexical_analyzer.token_types_simple as tokens_simple
import lexical_analyzer.errors as errors


#  Reserved keywords
RESERVED_KEYWORDS = {
    INTEGER_V: Token(INTEGER, INTEGER_V),
    FLOAT_V: Token(FLOAT, FLOAT_V),
    DOUBLE_V: Token(DOUBLE, DOUBLE_V),
    CHAR_V: Token(CHAR, CHAR_V),
    BOOL_V: Token(BOOL, BOOL_V),
    TRUE_V: Token(TRUE, TRUE_V),
    FALSE_V: Token(FALSE, FALSE_V),
    VOID_V: Token(VOID, VOID_V),
    IF_V: Token(IF, IF_V),
    ELSE_V: Token(ELSE, ELSE_V),
    SWITCH_V: Token(SWITCH, SWITCH_V),
    CASE_V: Token(CASE, CASE_V),
    FOR_V: Token(FOR, FOR_V),
    WHILE_V: Token(WHILE, WHILE_V),
    DO_V: Token(DO, DO_V),
    BREAK_V: Token(BREAK, BREAK_V),
    CONTINUE_V: Token(CONTINUE, CONTINUE_V),
    RETURN_V: Token(RETURN, RETURN_V),
    INCLUDE_V: Token(INCLUDE, INCLUDE_V),
    MAIN_V: Token(MAIN, MAIN_V),
    USING_V: Token(USING, USING_V),
    NAMESPACE_V: Token(NAMESPACE, NAMESPACE_V),
    ENDL_V: Token(ENDL, ENDL_V),
    COUT_V: Token(COUT, COUT_V),
}


class LexicalError(Exception):
    def __init__(self, line_num: int, column_num: int, message: str = errors.STANDARD_ERROR):
        self.line_num = line_num
        self.column_num = column_num
        self.message = errors.ERROR_CLASSIFICATION + f"{message}:{self.line_num}:{self.column_num}"
        super().__init__(self.message)


class Lexer:
    """Lexical analyzer
    Responsible for turning input string into set of Tokens
    """

    def __init__(self, code: str):
        self.pos = 0
        self.line_num = 1
        self.column_num = 0
        self.code = code
        self.current_char: str = self.code[self.pos]

        vars_ = vars(tokens_simple)
        tokens = {k: v for k, v in vars_.items() if not k.startswith('__')}.items()
        self.token_names = {k: v for k, v in tokens if not k.endswith('_V')}
        self.token_values = {k: v for k, v in tokens if k.endswith('_V')}

    def error(self, message) -> None:
        raise LexicalError(self.line_num, self.column_num, message)

    def move(self) -> None:
        """ Moves pointer and update 'current_char' """
        self.pos += 1
        if self.pos > len(self.code) - 1:
            self.current_char = None
        else:
            self.column_num += 1
            if self.current_char == '\n':
                self.line_num += 1
                self.column_num = 1
            self.current_char = self.code[self.pos]

    def peek(self) -> Union[str, None]:
        """ Check next character without moving pointer"""
        peek_pos = self.pos + 1
        if peek_pos > len(self.code) - 1:
            return None
        else:
            return self.code[peek_pos]

    def _id(self) -> Token:
        """ Handle identifiers and reserved keywords """
        result = ''
        while self.current_char is not None and self.current_char.isalnum() or self.current_char == '_':
            result += self.current_char
            self.move()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def skip_whitespaces(self) -> None:
        while self.current_char is not None and self.current_char.isspace():
            self.move()

    def skip_comment(self) -> None:
        """ Skip single line comment """
        self.move()
        self.move()
        while self.current_char is not None and self.current_char != '\n':
            self.move()
        self.move()

    def skip_multiline_comment(self) -> None:
        """ Skip multiline line comment """
        self.move()
        self.move()
        while self.current_char is not None \
                and self.current_char != COMMENT_MULTI_END_V[0] \
                and self.peek() == COMMENT_MULTI_END_V[1]:
            self.move()
        self.move()
        self.move()

    def number(self) -> Token:
        """ Parsing numbers into Token
        :return: mutlidigit integer, double or float consumed from the input
        """
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.move()

        # float number
        if self.current_char == '.':
            result += self.current_char
            self.move()

            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.move()

            # scientific notation
            if self.current_char == 'E':
                result += self.current_char
                self.move()
                if self.current_char == tokens_simple.PLUS_V or self.current_char == tokens_simple.MINUS_V:
                    result += self.current_char
                    self.move()

                while self.current_char is not None and self.current_char.isdigit():
                    result += self.current_char
                    self.move()
            elif self.current_char == 'f':
                self.move()
            token = Token(FLOAT_CONST, float(result))
        else:
            token = Token(INTEGER_CONST, int(result))
        return token

    def string(self) -> Token:
        """ Parsing string into Token
        Allows only double quote (")
        :return: Token(STRING_CONST, value)
        """
        result = ''

        self.move()
        while self.current_char != DOUBLE_QUOTE_V:
            if self.current_char is None:
                self.error(errors.UNCLOSED_DOUBLE_QUOTE)
            result += self.current_char
            self.move()
        self.move()

        token = Token(STRING_CONST, result)
        return token

    def char(self) -> Token:
        """ Parsing char into Token
        Allows only single quote (')
        :return: Token(CHAR_CONST, value)
        """
        self.move()
        result = self.current_char
        self.move()
        if self.current_char != SINGLE_QUOTE_V:
            self.error(errors.UNCLOSED_SINGLE_QUOTE)
        self.move()

        token = Token(CHAR_CONST, ord(result))
        return token

    def simple_token(self) -> Union[Token, None]:
        """ Symbols here will be simply handled as tokens with corresponding content
        No additional behavior is executed
        """
        for name in self.token_names:
            val = self.token_values.get(name + "_V")
            if len(val) == 1:
                if self.current_char == val:
                    self.move()
                    return Token(name, val)
            if len(val) == 2:
                if self.current_char == val[0] and self.peek() == val[1]:
                    self.move()
                    self.move()
                    return Token(name, val)
        return None

    def get_next_token(self) -> Token:
        """
        Lexical analyzer
        Breaks input into tokens one by one
        :return: current token
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespaces()
                continue

            if self.current_char == COMMENT_V[0] and self.peek() == COMMENT_V[1]:
                self.skip_comment()
                continue

            if self.current_char == COMMENT_MULTI_START_V[0] and self.peek() == COMMENT_MULTI_START_V[1]:
                self.skip_multiline_comment()
                continue

            if self.current_char.isalpha():
                return self._id()

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == DOUBLE_QUOTE_V:
                return self.string()

            if self.current_char == SINGLE_QUOTE_V:
                return self.char()

            token = self.simple_token()
            if token is None:
                self.error()
            return token

        return Token(EOF, None)
