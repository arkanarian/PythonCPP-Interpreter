from typing import Any, Union

from lexical_analyzer.tokens import *


class Lexer:
    """Lexical analyzer
    Responsible for turning input string into set of Tokens
    """

    def __init__(self, code: str):
        self.code: str = code
        self.pos = 0
        self.line_num = 0
        self.column_num = 0
        self.current_char: str = self.code[self.pos]

    def error(self) -> None:
        raise Exception(f"Invalid character:{self.line_num}:{self.column_num}")

    def move(self) -> None:
        """Moves pointer and update current_char"""
        self.pos += 1
        if self.pos > len(self.code) - 1:
            self.current_char = None
        else:
            self.current_char = self.code[self.pos]
            self.column_num += 1
            if self.current_char == '\n':
                self.line_num += 1
                self.column_num = 0

    def skip_whitespaces(self) -> None:
        while self.current_char is not None and self.current_char.isspace():
            self.move()

    def skip_comment(self) -> None:
        while self.current_char != '\n':
            self.move()
        self.move()

    def number(self) -> Token:
        """Parsing numbers into Token
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
                if self.current_char == '+' or self.current_char == '-':
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

    def char_string(self) -> Token:
        """Parsing character into Token
        Allows either single quote (') or double quote (")
        :return: character string
        """
        result = ''

        quote = self.current_char
        self.move()
        while self.current_char is not None and self.current_char != quote:
            result += self.current_char
            self.move()
        self.move()

        if quote == SINGLE_QUOTE_V:
            token = Token(CHAR_SINGLE_CONST, result)
        elif quote == DOUBLE_QUOTE_V:
            token = Token(CHAR_MULTI_CONST, result)
        else:
            self.error()

        return token

    def peek(self) -> Union[str, None]:
        peek_pos = self.pos + 1
        if peek_pos > len(self.code) - 1:
            return None
        else:
            return self.code[peek_pos]

    def _id(self) -> Token:
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.move()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def get_next_token(self) -> Token:
        """

        :return: current token
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespaces()
                continue

            if self.current_char == COMMENT_V[0] and self.peek() == COMMENT_V[1]:
                self.move()
                self.move()
                self.skip_comment()
                continue

            if self.current_char.isalpha():
                return self._id()

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == ASSIGN_V:
                self.move()
                return Token(ASSIGN, ASSIGN_V)

            if self.current_char == SINGLE_QUOTE_V or self.current_char == DOUBLE_QUOTE_V:
                return self.char_string()

            if self.current_char == SEMI_V:
                self.move()
                return Token(SEMI, SEMI_V)

            if self.current_char == COLON_V:
                self.move()
                return Token(COLON, COLON_V)

            if self.current_char == COMMA_V:
                self.move()
                return Token(COMMA, COMMA_V)

            if self.current_char == PLUS_V:
                self.move()
                return Token(PLUS, PLUS_V)

            if self.current_char == MINUS_V:
                self.move()
                return Token(MINUS, MINUS_V)

            if self.current_char == ASTERISK_V:
                self.move()
                return Token(ASTERISK, ASTERISK_V)

            if self.current_char == FORWARD_SLASH_V:
                self.move()
                return Token(FORWARD_SLASH, FORWARD_SLASH_V)

            if self.current_char == LBRACE_V:
                self.move()
                return Token(LBRACE, LBRACE_V)

            if self.current_char == RBRACE_V:
                self.move()
                return Token(RBRACE, RBRACE_V)

            if self.current_char == DOT_V:
                self.move()
                return Token(DOT, DOT_V)

            self.error()

        return Token(EOF, None)
