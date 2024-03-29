from interpreter.node_visitor import NodeVisitor
from syntax_analyzer.tree import *


class GraphTree(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.tabs = 0

    def visit(self, node: AST):
        self.tabs += 1
        super().visit(node)
        self.tabs -= 1

    def print(self, string: str):
        print(" | "*self.tabs + string)

    def visit_binop(self, node: BinOp):
        self.print("BinOp:")
        self.visit(node.right)
        self.print(node.op.value)
        self.visit(node.left)

    def visit_unaryop(self, node: UnaryOp):
        self.print("UnaryOp:")
        self.print(node.op.value)
        self.visit(node.expr)

    def visit_postfixop(self, node: PostfixOp):
        self.print("PostfixOp:")
        self.print(node.op.value)
        self.visit(node.expr)

    def visit_prefixop(self, node: PrefixOp):
        self.print("PrefixOp:")
        self.print(node.op.value)
        self.visit(node.expr)

    def visit_variable(self, node: Variable):
        self.print("Var name:")
        self.print(str(node.value))

    def visit_num(self, node: Num):
        self.print(str(node.value))

    def visit_string(self, node: String):
        self.print('"' + str(node.value) + '"')

    def visit_bool(self, node: Bool):
        self.print(str(node.value))

    def visit_compound(self, node: Compound):
        for child in node.children:
            self.visit(child)

    def visit_conditionstatement(self, node: ConditionStatement):
        self.print("If statement:")
        self.print("Condition:")
        self.visit(node.condition)
        self.print("If body:")
        self.visit(node.if_body)
        self.print("Else body:")
        self.visit(node.else_body)

    def visit_forstatement(self, node: ForStatement):
        self.print("ForStatement:")
        self.print("Init:")
        self.visit(node.init)
        self.print("Condition:")
        self.visit(node.condition)
        self.print("Action:")
        self.visit(node.action)
        self.print("For Body:")
        self.visit(node.body)

    def visit_whilestatement(self, node: WhileStatement):
        self.print("While Statement:")
        self.print("Condition:")
        self.visit(node.condition)
        self.print("For Body:")
        self.visit(node.body)

    def visit_dowhilestatement(self, node: DoWhileStatement):
        self.print("Do While Statement:")
        self.print("Condition:")
        self.visit(node.condition)
        self.print("For Body:")
        self.visit(node.body)

    def visit_breakstatement(self, node: BreakStatement):
        self.print("Break Statement")

    def visit_continuestatement(self, node: ContinueStatement):
        self.print("Continue Statement")

    def visit_returnstatement(self, node: ReturnStatement):
        self.print("Break Statement")
        self.visit(node.expr)

    def visit_switchcompound(self, node: SwitchCompound):
        self.print("Switch Compound")
        self.print("condition:")
        self.visit(node.condition)
        self.print("body:")
        self.visit(node.body)

    def visit_switchstatement(self, node: SwitchStatement):
        self.print("Switch Statement")
        self.print("condition:")
        self.visit(node.condition)
        self.print("body:")
        for statement in node.case_statements:
            self.visit(statement)
        self.print("default:")
        self.visit(node.default_statement)

    def visit_noop(self, node: NoOp):
        pass

    def visit_imports(self, node: Imports):
        self.print("Include imports:")
        for include_node in node.include_nodes:
            self.visit(include_node)
        self.print("Using imports:")
        for using_node in node.using_nodes:
            self.visit(using_node)

    def visit_type(self, node: Type):
        self.print("Type:")
        self.print(node.value)

    def visit_assign(self, node: Assign):
        self.print("Assign:")
        self.visit(node.left)
        self.print(node.op.value)
        self.visit(node.right)

    def visit_vardecl(self, node: VarDecl):
        self.print("VarDecl:")
        self.visit(node.var_node)
        self.visit(node.type_node)

    def visit_print(self, node: Print):
        self.print("Print:")
        for child in node.children:
            self.visit(child)

    def visit_ternaryop(self, node: TernaryOp):
        self.print("Assign:")
        self.print("Condition:")
        self.visit(node.condition)
        self.print("First expr:")
        self.visit(node.first_expr)
        self.print("Second expr:")
        self.visit(node.second_expr)

    def visit_mainfunction(self, node: MainFunction):
        self.print("Main function:")
        self.visit(node.compound_statement)

    def visit_program(self, node: Program):
        self.print("Program:")
        self.print("Imports:")
        self.visit(node.imports_node)
        self.print("Statements_before:")
        for decl in node.declarations_before:
            self.visit(decl)
        self.visit(node.main_function)
        self.print("Statements_after:")
        for decl in node.declarations_after:
            self.visit(decl)

    def print_tree(self):
        self.visit(self.tree)
