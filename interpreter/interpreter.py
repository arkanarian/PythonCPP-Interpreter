from syntax_analyzer.tree import Program, MainFunction, Compound, BinOp
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

