from lexical_analyzer.token_types import EOF


class PrintTokens:
    def __init__(self, lexer):
        self.lexer = lexer
        self.token = None

    def print(self):
        while True:
            cur_line = self.lexer.line_num
            print(f"/{cur_line}:  ", end="")
            print(self.token, end=",") if self.token is not None else None
            self.token = self.lexer.get_next_token()
            while self.lexer.line_num == cur_line:
                print(self.token, end=",")
                if self.token.type == EOF:
                    break
                self.token = self.lexer.get_next_token()
            if self.token.type == EOF:
                break
            print()
