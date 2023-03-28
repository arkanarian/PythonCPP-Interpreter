from typing import Sequence, Union, TypeVar, Optional

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


class PostfixOp(AST):
    def __init__(self, op: Token, expr: ASTNode):
        self.token = self.op = op
        self.expr = expr


class PrefixOp(AST):
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


class ConditionLoop(AST):
    def __init__(self, left, token: Token, right):
        self.left = left
        self.token = token
        self.right = right


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
        self.children = []


class MainFunction(AST):
    def __init__(self, compound_statement: Compound, name_node):
        self.name_node = name_node
        self.compound_statement = compound_statement


class Imports(AST):
    def __init__(self):
        self.include_nodes = []
        self.using_nodes = []


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


class VarDecl(AST):
    def __init__(self, var_node: Variable, type_node: Type):
        self.var_node = var_node
        self.type_node = type_node


class Print(AST):
    def __init__(self):
        self.children = []


class TernaryOp(AST):
    def __init__(self, condition, first_expr, second_expr):
        self.condition = condition
        self.first_expr = first_expr
        self.second_expr = second_expr


class Program(AST):
    def __init__(self, imports: Imports, declarations_before: Sequence[ASTNode], main_function: MainFunction, declarations_after: Sequence[ASTNode]):
        self.imports_node = imports
        self.declarations_before = declarations_before
        self.main_function = main_function
        self.declarations_after = declarations_after


class ConditionStatement(AST):
    def __init__(self, condition, if_body, else_body):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body


class ForStatement(AST):
    def __init__(self, init, condition, action, body):
        self.init = init
        self.condition = condition
        self.action = action
        self.body = body


class WhileStatement(AST):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class DoWhileStatement(AST):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class BreakStatement(AST):
    pass


class ContinueStatement(AST):
    pass


class ReturnStatement(AST):
    def __init__(self, expr):
        self.expr = expr


class SwitchCompound(AST):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class SwitchStatement(AST):
    def __init__(self, condition, case_statements, default_statement):
        self.condition = condition
        self.case_statements = case_statements
        self.default_statement = default_statement
