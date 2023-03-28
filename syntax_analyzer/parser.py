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
        raise SyntaxError(self.lexer.line_num, self.lexer.column_num-1, message)

    def eat(self, token_type: str) -> None:
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(errors.NOT_EXPECTED_TOKEN(token_type, self.current_token.type))

    @buffer
    def is_main(self):
        self.eat(self.current_token.type)
        if self.current_token.type != ID:
            return False
        self.eat(ID)
        return self.current_token.type == LPAREN

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
        # if self.current_token.type == ID:
        #     node = self.assign_statement()
        if self.current_token.type == IF:
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
            node = self.expr_statement()
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
        if self.current_token.type == RETURN:
            self.eat(RETURN)
            expr = self.empty()
            if self.current_token.type != SEMI:
                expr = self.expr()
            self.eat(SEMI)
            return ReturnStatement(expr=expr)
        elif self.current_token.type == BREAK:
            self.eat(BREAK)
            self.eat(SEMI)
            return BreakStatement()
        elif self.current_token.type == CONTINUE:
            self.eat(CONTINUE)
            self.eat(SEMI)
            return ContinueStatement()

    def if_statement(self):
        self.eat(IF)
        self.eat(LPAREN)
        condition = self.expr()
        self.eat(RPAREN)
        if_body = self.statement()
        else_body = self.empty()
        if self.current_token.type == ELSE:
            self.eat(ELSE)
            else_body = self.statement()
        return ConditionStatement(condition=condition, if_body=if_body, else_body=else_body)

    def switch_statement(self):
        self.eat(SWITCH)
        self.eat(LPAREN)
        condition = self.expr()
        self.eat(RPAREN)
        self.eat(LBRACKET)
        case_statements = []
        default_statement = self.empty()
        while self.current_token.type == CASE:
            case_statements.append(self.case_statement())
        if self.current_token.type == DEFAULT:
            default_statement = self.default_statement()
        self.eat(RBRACKET)
        return SwitchStatement(condition=condition, case_statements=case_statements, default_statement=default_statement)

    def case_statement(self):
        self.eat(CASE)
        condition = self.empty()
        if self.current_token.type == ID:
            condition = self.variable()
        else:
            condition = self.constant()
        self.eat(COLON)
        body = self.statement()
        return SwitchCompound(condition=condition, body=body)

    def default_statement(self):
        self.eat(DEFAULT)
        self.eat(COLON)
        body = self.statement()
        return SwitchCompound(condition=self.empty(), body=body)

    def loop_statement(self):
        if self.current_token.type == WHILE:
            self.eat(WHILE)
            self.eat(LPAREN)
            condition = self.expr()
            self.eat(RPAREN)
            body = self.statement()
            return WhileStatement(condition=condition, body=body)
        elif self.current_token.type == DO:
            self.eat(DO)
            body = self.statement()
            self.eat(WHILE)
            self.eat(LPAREN)
            condition = self.expr()
            self.eat(RPAREN)
            self.eat(SEMI)
            return DoWhileStatement(condition=condition, body=body)
        else:
            self.eat(FOR)
            self.eat(LPAREN)
            print(self.current_token.type)
            if self.current_token.type in [INTEGER, FLOAT, CHAR, STRING, BOOL]:
                init = self.declaration_list()[0]
            else:
                init = self.expr_statement()
            condition = self.expr_statement()
            if self.current_token.type == RPAREN:
                action = self.empty()
            else:
                action = self.expr()
            self.eat(RPAREN)
            body = self.statement()
            return ForStatement(init=init, condition=condition, action=action, body=body)

    # def init_loop_statement(self):
    #     node = self.empty()
    #     if self.current_token.type != SEMI:
    #         if self.current_token.type in [INTEGER, FLOAT, CHAR, STRING]:
    #             node = self.declaration_list()
    #         elif self.current_token.type == ID:
    #             node = self.assign_statement()
    #     self.eat(SEMI)
    #     return node
    #
    # def condition_loop_statement(self):
    #     node = self.empty()
    #     if self.current_token.type != SEMI:
    #         left = self.factor()
    #         if self.current_token.type in [EQUAL, NOT_EQUAL, LESS, GREATER, LE_OP, GE_OP]:
    #             op = self.current_token
    #             self.eat(self.current_token.type)
    #         right = self.factor()
    #     self.eat(SEMI)
    #     return node
    #
    # def inc_loop_statement(self):
    #     node = self.empty()
    #     token = ""
    #     if self.current_token.type in [DEC_OP, INC_OP]:
    #         self.eat(self.current_token.type)
    #         node = self.variable()
    #     elif self.current_token.type == ID:
    #         node = self.variable()
    #         if self.current_token.type in [INC_OP, DEC_OP]:
    #             token = self.current_token
    #         elif self.current_token.type == RPAREN:
    #
    #     else:
    #         node = self.assign_statement()
    #     return UnaryOp(token, node)

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

    def expr(self):
        node = self.ternary_operator()
        return node

    @buffer
    def check_assign_statement(self):
        if self.current_token.type != ID:
            return False
        self.eat(self.current_token.type)
        return self.current_token.type in [ASSIGN, PLUS_ASSIGN, MINUS_ASSIGN, MUL_ASSIGN, DIVIDE_ASSIGN, MOD_ASSIGN, XOR_ASSIGN]

    def expr_statement(self):
        node = self.empty()
        if self.current_token.type != SEMI:
            if self.check_assign_statement():
                node = self.assign_statement()
                return node
            else:
                node = self.expr()
        self.eat(SEMI)
        return node

    def ternary_operator(self) -> ASTNode:
        node = self.logical_or()
        if self.current_token.type == QUESTION_MARK:
            self.eat(QUESTION_MARK)
            expr = self.expr()
            self.eat(COLON)
            return TernaryOp(condition=node, first_expr=expr, second_expr=self.ternary_operator())
        return node

    def logical_or(self):
        node = self.logical_and()
        while self.current_token.type == LOG_OR:
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.logical_and())
        return node

    def logical_and(self):
        node = self.bitwise_or()
        while self.current_token.type == LOG_AND:
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.bitwise_or())
        return node

    def bitwise_or(self):
        node = self.bitwise_xor()
        while self.current_token.type == OR_OP:
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.bitwise_xor())
        return node

    def bitwise_xor(self):
        node = self.bitwise_and()
        while self.current_token.type == XOR_OP:
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.bitwise_and())
        return node

    def bitwise_and(self):
        node = self.equality_ops()
        while self.current_token.type == XOR_OP:
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.equality_ops())
        return node

    def equality_ops(self):
        node = self.comparison_ops()
        while self.current_token.type in [EQUAL, NOT_EQUAL]:
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.comparison_ops())
        return node

    def comparison_ops(self):
        node = self.left_right_ops()
        while self.current_token.type in [EQUAL, NOT_EQUAL]:
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.left_right_ops())
        return node

    def left_right_ops(self):
        node = self.add_sub_ops()
        while self.current_token.type in [LEFT_OP, RIGHT_OP]:
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.add_sub_ops())
        return node

    def add_sub_ops(self):
        """add_sub_ops             : mul_div_mod_ops ((PLUS | MINUS) mul_div_mod_ops)*"""
        node = self.mul_div_mod_ops()
        while self.current_token.type in [PLUS, MINUS]:
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.mul_div_mod_ops())
        return node

    def mul_div_mod_ops(self):
        """mul_div_mod_ops         : cast_operator ((MUL | DIV | MOD) cast_operator)*"""
        node = self.cast_operator()
        while self.current_token.type in [ASTERIKS, DIVIDE, MOD]:
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.cast_operator())
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
            return self.prefix_operator_rep()
        elif self.current_token.type in [PLUS, MINUS, LOG_NOT, NOT_OP, AND_OP]:
            token = self.current_token
            self.eat(token.type)
            expr = self.cast_operator()
            return UnaryOp(op=token, expr=expr)
        return self.postfix_operator()

    def prefix_operator_rep(self) -> ASTNode:
        if self.current_token.type in [INC_OP, DEC_OP]:
            token = self.current_token
            self.eat(token.type)
            expr = self.prefix_operator_rep()
            return PrefixOp(op=token, expr=expr)
        else:
            return self.variable()

    # def postfix_operator_rep(self, var: Variable) -> ASTNode:
    #     if self.current_token.type in [INC_OP, DEC_OP]:
    #         token = self.current_token
    #         self.eat(token.type)
    #         node = self.postfix_operator_rep(var)
    #         return PostfixOp(op=token, expr=node)
    #     else:
    #         return var

    def postfix_operator(self) -> ASTNode:
        node = self.factor()
        if self.current_token.type in [INC_OP, DEC_OP]:
            if not isinstance(node, Variable):
                self.error("Left value should be variable")
            token = self.current_token
            self.eat(token.type)
            return PostfixOp(op=token, expr=node)
            # if self.current_token.type in [INC_OP, DEC_OP]:
            #     return PostfixOp(op=token, expr=self.postfix_operator_rep(node))
            # else:
            #     return PostfixOp(op=token, expr=node)
        return node

    def factor(self) -> ASTNode:
        token = self.current_token
        if token.type == LPAREN:
            self.eat(LPAREN)
            expr = self.expr()
            self.eat(RPAREN)
            return expr
        elif token.type in [INTEGER_CONST, FLOAT_CONST, CHAR_CONST, STRING_CONST, TRUE, FALSE]:
            return self.constant()
        else:
            return self.variable()

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

    def type_spec(self) -> Type:
        token = self.current_token
        if token.type in [INTEGER, FLOAT, DOUBLE, CHAR, STRING, BOOL]:
            self.eat(token.type)
            return Type(token)

    def variable(self) -> Variable:
        node = Variable(token=self.current_token)
        self.eat(ID)
        return node

    def empty(self) -> NoOp:
        return NoOp()

    def parse(self) -> ASTNode:
        node = self.program()
        print(node)
        if self.current_token.type != EOF:
            self.error(errors.NOT_EXPECTED_TOKEN(EOF, self.current_token.type))

        return node
