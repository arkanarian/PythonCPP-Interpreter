import argparse
from pathlib import Path

from syntax_analyzer.parser import Parser, SyntaxError
from lexical_analyzer.lexer import Lexer, LexicalError

import os
import sys


# path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
# sys.path.append(os.path.join(path))


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("path")
    # args = parser.parse_args()
    file_path = Path(path + "/tests/test_parser.cpp")
    with open(file_path, 'r') as f:
        code_lines = f.readlines()
        code = ''.join(code_lines)
    try:
        lexer = Lexer(code)
        from tests.print_tokens import PrintTokens
        print_tokens = PrintTokens(Lexer(code))
        print_tokens.print()
    except LexicalError as e:
        print()
        code_line = code_lines[e.line_num-1][:-1]
        print(code_line)
        print('~^~'.rjust(e.column_num+1))
        print(e)
        return
    parser = Parser(lexer)
    try:
        tree = parser.parse()
    except SyntaxError as e:
        print()
        code_line = code_lines[e.line_num-1][:-1]
        print(code_line)
        print('~^~'.rjust(e.column_num+1))
        print(e)
        return

    from tests.print_tree import GraphTree
    graphic_tree = GraphTree(tree)
    graphic_tree.visit(tree)


if __name__ == '__main__':
    main()