from typing import Sequence, Union, TypeVar

from lexical_analyzer.token import Token


class AST:
    pass


ASTNode = TypeVar("ASTNode", bound=AST)


class BinOp(AST):
    def __init__(self, left: ASTNode, op: Token, right: ASTNode):
        self.left = left
        self.token = self.op = op
        self.right = right


class UnaryOp(AST):
    def __init__(self, op: Token, expr: ASTNode):
        self.token = self.op = op
        self.expr = expr


class Variable(AST):
    """
    value - name of variable
    """
    def __init__(self, token: Token):
        self.token = token
        self.value = self.token.value


class Num(AST):
    """
    value - value of num
    """
    def __init__(self, token: Token):
        self.token = token
        self.value = self.token.value


class String(AST):
    """
    value - value of string
    """
    def __init__(self, token: Token):
        self.token = token
        self.value = self.token.value


class Bool(AST):
    """
    value - value of bool
    """
    def __init__(self, token: Token):
        self.token = token
        self.value = self.token.value


class Compound(AST):
    def __init__(self):
        self.statements = []


class MainFunction(AST):
    def __init__(self, compound_statement: Compound):
        self.compound_statement = compound_statement


class Import(AST):
    def __init__(self, includes: Sequence[Variable], usings: Sequence[Variable]):
        self.include_nodes = includes
        self.using_nodes = usings


class NoOp(AST):
    pass


class Type(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value


class Assign(AST):
    def __init__(self, left: Variable, op: Token, right):
        self.left = left
        self.op = op
        self.right = right


class TernaryOp(AST):
    def __init__(self, condition, first_expr, second_expr):
        self.condition = condition
        self.first_expr = first_expr
        self.second_expr = second_expr


class Program(AST):
    def __init__(self, imports: Sequence[Import], statements_before: Sequence[ASTNode], main_func: MainFunction, statements_after: Sequence[ASTNode]):
        self.imports_node = imports
        self.statements_before = statements_before
        self.main_func = main_func
        self.statements_after = statements_after
