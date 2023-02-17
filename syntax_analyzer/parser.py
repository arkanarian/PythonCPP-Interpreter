from typing import Optional, TypeVar

from lexical_analyzer.lexer import Lexer
from lexical_analyzer.token_types import *
from lexical_analyzer.token_types_simple import *
from lexical_analyzer.token import Token
import syntax_analyzer.errors as errors
from syntax_analyzer.tree import *
from utils.utils import buffer

ASTNode = TypeVar("ASTNode", bound=AST)


class SyntaxError(Exception):
    def __init__(self, line_num: int, column_num: int, message: str = errors.STANDARD_ERROR):
        self.line_num = line_num
        self.column_num = column_num
        self.message = errors.ERROR_CLASSIFICATION + f"{message}:{self.line_num}:{self.column_num}"
        super().__init__(self.message)


class Parser:
    """
    Parsing AST
    """
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token: Optional[Token] = self.lexer.get_next_token()

    def error(self, message):
        raise SyntaxError(0, 0, message)

    def eat(self, token_type: str) -> None:
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(errors.NOT_EXPECTED_TOKEN(token_type, self.current_token.type, self.lexer.line_num, self.lexer.column_num))

    @buffer
    def is_main(self):
        self.eat(self.current_token.type)
        return self.current_token.type == MAIN

    def program(self) -> Program:
        """ program : (imports | main_function | statement)* """
        statements_before = []
        statements_after = []
        imports = []
        while self.current_token.type in [USING, HASH]:
            imports.append(self.imports())

        while self.current_token.type in [INTEGER, FLOAT, DOUBLE, CHAR, BOOL] and not self.is_main():
            statements_before.append(self.statement())
        print(statements_before)

        if self.is_main():
            main_function = self.main_function()

        while self.current_token.type in [INTEGER, FLOAT, DOUBLE, CHAR, BOOL]:
            statements_after.append(self.statement())

        return Program(imports=imports, statements_before=statements_before)

    def imports(self):
        if self.current_token.type == USING:
            self.eat(USING)
            self.eat(NAMESPACE)
            name = self.variable()
            self.eat(SEMI)
            return name

        elif self.current_token.type == HASH:
            self.eat(HASH)
            self.eat(INCLUDE)
            self.eat(LESS)
            name = self.variable()
            self.eat(GREATER)
            return name

        else:
            self.empty()

    def main_function(self) -> MainFunction:
        self.eat(INTEGER)
        self.eat(MAIN)
        compound_statement = self.compound_statement()
        return MainFunction()


    def statement(self) -> ASTNode:
        """
        **statement**               : assign_statement
                            | declaration_statement
                            | compound_statement
                            | if_statement
                            | loop_statement
                            | jump_statement
                            | switch_statement
                            | print_statement
                            | empty
        """
        if self.current_token.type == ID:
            node = self.assign_statement()
        elif self.current_token.type in [INTEGER, FLOAT, DOUBLE, CHAR, BOOL]:
            node = self.declaration_statement()
        elif self.current_token.type == IF:
            node = self.if_statement()
        elif self.current_token.type == LBRACKET:
            node = self.compound_statement()
        elif self.current_token.type in [WHILE, DO, FOR]:
            node = self.loop_statement()
        elif self.current_token.type in [RETURN, BREAK, CONTINUE]:
            node = self.jump_statement()
        elif self.current_token.type == SWITCH:
            node = self.switch_statement()
        elif self.current_token.type == COUT:
            node = self.print_statement()
        else:
            node = self.empty()
        return node

    def compound_statement(self) -> Compound:
        """**compound_statement**      : LBRACKET statement* RBRACKET"""
        statement_list = []
        self.eat(LBRACKET)
        while self.current_token.type is not RBRACKET:
            statement_list.append(self.statement())
        self.eat(RBRACKET)
        compound = Compound()
        for statement in statement_list:
            compound.children.append(self.statement())
        return compound

    def jump_statement(self):
        pass

    def if_statement(self):
        pass

    def switch_statement(self):
        pass

    def loop_statement(self):
        pass

    def assign_statement(self):
        left = self.variable()
        op = self.current_token
        if op.type == ASSIGN:
            self.eat(ASSIGN)
        elif op.type == PLUS_ASSIGN:
            self.eat(PLUS_ASSIGN)
        elif op.type == MINUS_ASSIGN:
            self.eat(MINUS_ASSIGN)
        elif op.type == MUL_ASSIGN:
            self.eat(MUL_ASSIGN)
        elif op.type == DIVIDE_ASSIGN:
            self.eat(DIVIDE_ASSIGN)
        elif op.type == MOD_ASSIGN:
            self.eat(MOD_ASSIGN)
        elif op.type == XOR_ASSIGN:
            self.eat(XOR_ASSIGN)
        right = self.expr()
        self.eat(SEMI)
        return Assign(left=left, op=op, right=right)

    def declaration_statement(self):
        type_node = self.type_spec()
        var_nodes = [self.variable()]
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            var_nodes.append(self.variable())
            
        declaration_list = self.declaration_list()

    def declaration_list(self):
        pass

    def declaration(self):
        pass

    def print_statement(self):
        pass

    def expr(self) -> TernaryOp:
        node = self.ternary_operator()
        return node

    def ternary_operator(self) -> ASTNode:
        node = self.logical_or()
        if self.current_token.type == QUESTION_MARK:
            self.eat(QUESTION_MARK)
            expr = self.expr()
            self.eat(COLON)
            second_expr = self.ternary_operator()
            return TernaryOp(condition=node, first_expr=expr, second_expr=second_expr)
        return node

    def logical_or(self):
        node = self.logical_and()
        if self.current_token.type == LOG_OR:
            token = self.current_token
            self.eat(token.type)
            return BinOp(left=node, op=token, right=self.logical_and())
        return node

    def logical_and(self):
        node = self.bitwise_or()
        if self.current_token.type == LOG_AND:
            token = self.current_token
            self.eat(token.type)
            return BinOp(left=node, op=token, right=self.bitwise_or())
        return node

    def bitwise_or(self):
        node = self.bitwise_xor()
        if self.current_token.type == OR_OP:
            token = self.current_token
            self.eat(token.type)
            return BinOp(left=node, op=token, right=self.bitwise_xor())
        return node

    def bitwise_xor(self):
        node = self.bitwise_and()
        if self.current_token.type == XOR_OP:
            token = self.current_token
            self.eat(token.type)
            return BinOp(left=node, op=token, right=self.bitwise_and())
        return node

    def bitwise_and(self):
        node = self.equality_ops()
        if self.current_token.type == XOR_OP:
            token = self.current_token
            self.eat(token.type)
            return BinOp(left=node, op=token, right=self.equality_ops())
        return node

    def equality_ops(self):
        node = self.comparison_ops()
        if self.current_token.type in [EQUAL, NOT_EQUAL]:
            token = self.current_token
            self.eat(token.type)
            return BinOp(left=node, op=token, right=self.comparison_ops())
        return node

    def comparison_ops(self):
        node = self.left_right_ops()
        if self.current_token.type in [EQUAL, NOT_EQUAL]:
            token = self.current_token
            self.eat(token.type)
            return BinOp(left=node, op=token, right=self.left_right_ops())
        return node

    def left_right_ops(self):
        node = self.add_sub_ops()
        if self.current_token.type in [LEFT_OP, RIGHT_OP]:
            token = self.current_token
            self.eat(token.type)
            return BinOp(left=node, op=token, right=self.add_sub_ops())
        return node

    def add_sub_ops(self):
        node = self.mul_div_mod_ops()
        if self.current_token.type in [PLUS, MINUS]:
            token = self.current_token
            self.eat(token.type)
            return BinOp(left=node, op=token, right=self.mul_div_mod_ops())
        return node

    def mul_div_mod_ops(self):
        node = self.cast_operator()
        if self.current_token.type in [ASTERIKS, DIVIDE, MOD]:
            token = self.current_token
            self.eat(token.type)
            return BinOp(left=node, op=token, right=self.cast_operator())
        return node

    @buffer
    def check_cast_expression_pre(self):
        if self.current_token.type == LPAREN:
            self.eat(LPAREN)
            if self.current_token.type in [INTEGER, DOUBLE, FLOAT, CHAR]:
                self.eat(self.current_token.type)
                return self.current_token.type == RPAREN
        return False

    @buffer
    def check_cast_expression_post(self):
        if self.current_token.type in [INTEGER, DOUBLE, FLOAT, CHAR]:
            self.eat(self.current_token.type)
            return self.current_token.type == LPAREN
        return False

    def cast_operator(self) -> ASTNode:
        if self.check_cast_expression_pre():
            self.eat(LPAREN)
            type_node = self.type_spec()
            self.eat(RPAREN)
            expr = self.cast_operator()
            return UnaryOp(op=type_node.token, expr=expr)

        elif self.check_cast_expression_post():
            type_node = self.type_spec()
            self.eat(LPAREN)
            expr = self.cast_operator()
            self.eat(RPAREN)
            return UnaryOp(op=type_node.token, expr=expr)

        return self.unary_operator()

    def unary_operator(self) -> ASTNode:
        if self.current_token.type in [INC_OP, DEC_OP]:
            token = self.current_token
            self.eat(token.type)
            expr = self.postfix_operator()
            return UnaryOp(op=token, expr=expr)
        elif self.current_token.type in [PLUS, MINUS, LOG_NOT, NOT_OP, AND_OP]:
            token = self.current_token
            self.eat(token.type)
            expr = self.cast_operator()
            return UnaryOp(op=token, expr=expr)
        return self.postfix_operator()

    def postfix_operator(self) -> ASTNode:
        node = self.factor()
        if self.current_token.type in [INC_OP, DEC_OP]:
            token = self.current_token
            self.eat(token.type)
            return UnaryOp(op=token, expr=node)
        return node

    def factor(self) -> ASTNode:
        token = self.current_token
        if token.type == ID:
            return self.variable()
        elif token.type == LPAREN:
            self.eat(LPAREN)
            expr = self.expr()
            self.eat(RPAREN)
        else:
            return self.constant()

    def type_spec(self) -> Type:
        token = self.current_token
        if token.type in [INTEGER, FLOAT, DOUBLE, CHAR, BOOL]:
            self.eat(token.type)
            return Type(token.type)

    def empty(self) -> None:
        pass

    def variable(self) -> Variable:
        node = Variable(token=self.current_token)
        self.eat(ID)
        return node

    def constant(self) -> Union[Num, String, Bool]:
        token = self.current_token
        if token.type in [INTEGER_CONST, FLOAT_CONST, DOUBLE_CONST, CHAR_CONST]:
            self.eat(token.type)
            return Num(token)
        elif token.type == STRING_CONST:
            self.eat(token.type)
            return String(token)
        elif token.type in [TRUE, FALSE]:
            self.eat(token.type)
            return Bool(token)

    def parse(self) -> ASTNode:
        node = self.program()
        print(node)
        if self.current_token.type != EOF:
            self.error(errors.NOT_EXPECTED_TOKEN(EOF, self.current_token))

        return node