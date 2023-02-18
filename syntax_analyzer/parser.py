from typing import Optional, TypeVar, List

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
        if self.current_token.type != ID:
            return False
        self.eat(ID)
        return self.current_token.type == LPAREN

    # @buffer
    # def is_string(self):
    #     if self.current_token.type != ID and self.current_token.value != CONST_V:
    #         return False
    #     self.eat(ID)
    #     if self.current_token.type != ID and self.current_token.value != CHAR_V:
    #         return False
    #     self.eat(ID)
    #     return self.current_token.type == ASTERIKS

    def program(self) -> Program:
        """ program : (imports | main_function | statement)* """
        declarations_before = []
        declarations_after = []
        imports_node = Imports()
        while self.current_token.type in [USING, INCLUDE, INTEGER, FLOAT, DOUBLE, CHAR, STRING, BOOL] and not self.is_main():
            if self.current_token.type == USING:
                imports_node.using_nodes.append(self.imports_using())
            elif self.current_token.type == INCLUDE:
                imports_node.include_nodes.append(self.imports_include())
            else:
                declarations_before.extend(self.declaration_list())
        print(declarations_before)

        main_function = None
        if self.is_main():
            main_function = self.main_function()

        while self.current_token.type in [INTEGER, FLOAT, DOUBLE, CHAR, STRING, BOOL]:
            declarations_after.extend(self.declaration_list())

        return Program(imports=imports_node, declarations_before=declarations_before, main_function=main_function, declarations_after=declarations_after)

    def imports_using(self):
        self.eat(USING)
        self.eat(NAMESPACE)
        token = self.variable()
        self.eat(SEMI)
        return token

    def imports_include(self):
        self.eat(INCLUDE)
        self.eat(LESS)
        token = self.variable()
        self.eat(GREATER)
        return token

    def main_function(self) -> MainFunction:
        self.eat(INTEGER)
        name_node = self.variable()
        self.eat(LPAREN)
        self.eat(RPAREN)
        compound_statement = self.compound_statement()
        return MainFunction(compound_statement=compound_statement, name_node=name_node)

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
        """ compound_statement      : LBRACKET statement* RBRACKET """
        result = []
        compound = Compound()
        self.eat(LBRACKET)
        while self.current_token.type != RBRACKET:
            if self.current_token.type in [INTEGER, FLOAT, DOUBLE, CHAR, STRING, BOOL]:
                result.extend(self.declaration_list())
            else:
                result.append(self.statement())
        self.eat(RBRACKET)
        for child in result:
            compound.children.append(child)
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

    def declaration_list(self) -> List[Union[VarDecl, Assign]]:
        """ declaration_list        : type_spec declaration (COMMA declaration)* SEMI """
        result = []
        type_node = self.type_spec()
        result.extend(self.declaration())
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            result.extend(self.declaration())
        self.eat(SEMI)

        # ФИЧА: преобразуем List[Union[Assign, Variable]] в List[Union[VarDecl, Assign]]
        # используя type_node при замене VarDecl
        return_result = []
        for node in result:
            if isinstance(node, Variable):
                return_result.append(VarDecl(type_node=type_node, var_node=node))
            else:
                return_result.append(node)

        return return_result

    def declaration(self) -> List[Union[Variable, Assign]]:
        """ declaration             : variable (ASSIGN expr)? """
        result = []
        var_node = self.variable()
        result.append(var_node)
        if self.current_token.type == ASSIGN:
            token = self.current_token
            self.eat(token.type)
            expr = self.expr()
            result.append(Assign(left=var_node, op=token, right=expr))
        return result

    def print_statement(self):
        result = []
        print_node = Print()
        self.eat(COUT)
        self.eat(LEFT_OP_COUT)
        result.append(self.expr())
        while self.current_token.type == LEFT_OP_COUT:
            self.eat(LEFT_OP_COUT)
            result.append(self.expr())
        self.eat(SEMI)
        [print_node.children.append(node) for node in result]
        return print_node


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
            if self.current_token.type in [INTEGER, DOUBLE, FLOAT, CHAR, STRING, BOOL]:
                self.eat(self.current_token.type)
                return self.current_token.type == RPAREN
        return False

    @buffer
    def check_cast_expression_post(self):
        if self.current_token.type in [INTEGER, DOUBLE, FLOAT, CHAR, STRING, BOOL]:
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
        if token.type in [INTEGER, FLOAT, DOUBLE, CHAR, STRING, BOOL]:
            self.eat(token.type)
            return Type(token)

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