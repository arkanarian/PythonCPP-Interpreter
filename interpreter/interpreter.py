import argparse
from pathlib import Path

import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(path))

from lexical_analyzer.token_types import EOF
from lexical_analyzer.lexer import Lexer, LexicalError


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    file_path = Path(args.path)
    print(file_path)
    with open(file_path, 'r') as f:
        code_lines = f.readlines()
        code = ''.join(code_lines)
        print(code)
    lexer = Lexer()
    while True:
        try:
            token = lexer.get_next_token()
            print(token)
            if token.type == EOF:
                break
        except LexicalError as e:
            print()
            code_line = code_lines[e.line_num-1][:-1]
            print(code_line)
            print('~^~'.rjust(e.column_num+1))
            print(e)
            break


if __name__ == '__main__':
    main()
