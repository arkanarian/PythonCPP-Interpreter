import argparse
from pathlib import Path

import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(path))

from syntax_analyzer.parser import Parser
from syntax_analyzer.tree import Program, MainFunction, Compound, BinOp
from lexical_analyzer.lexer import Lexer, LexicalError
from node_visitor import NodeVisitor


class Interpreter(NodeVisitor):
    def __init__(self):
        pass

    def visit_program(self, node: Program):
        for import_node in node.imports_node:
            self.visit(import_node)
        for statement_node in node.statements_before:
            self.visit(statement_node)
        self.visit(node.main_func)
        for statement_node in node.statements_after:
            self.visit(statement_node)

    def visit_mainfunction(self, node: MainFunction):
        self.visit(node.compound_statement)

    def visit_compound(self, node: Compound):
        for child in node.statements:
            self.visit(child)

    def visit_binop(self, node: BinOp):
        self.visit(node.right)
        self.visit(node.left)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    file_path = Path(args.path)
    with open(file_path, 'r') as f:
        code_lines = f.readlines()
        code = ''.join(code_lines)
    try:
        lexer = Lexer(code)
    except LexicalError as e:
        print()
        code_line = code_lines[e.line_num-1][:-1]
        print(code_line)
        print('~^~'.rjust(e.column_num+1))
        print(e)
        return
    parser = Parser(lexer)
    tree = parser.parse()
    from tests.print_tree import GraphTree
    graphic_tree = GraphTree(tree)
    graphic_tree.visit(tree)


if __name__ == '__main__':
    main()
