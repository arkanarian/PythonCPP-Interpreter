
**program**                 : (imports_using | imports_include | declaration_list)* main_function (declaration_list)*

**imports_using**           : USING NAMESPACE variable SEMI

**imports_include**         : HASH INCLUDE LESS variable GRATER
    
**main_function**           : INTEGER variable compound_statement

**statement**               : assign_statement
                            | compound_statement
                            | if_statement
                            | loop_statement
                            | jump_statement
                            | switch_statement
                            | print_statement
                            | expr_statement
                            | empty

**compound_statement**      : LBRACKET (declaration_list | statement)* RBRACKET

**jump_statement**          : RETURN expression? SEMI
                            | BREAK SEMI    
                            | CONTINUE SEMI

**if_statement**            : IF LPAREN expr RPAREN statement (ELSE statement)?

**switch_statement**        : SWITCH LPAREN expr RPAREN LBRACKET case_statement* (default_statement)? RBRACKET

**switch_compound**         : CASE (constant | variable) COLON statement

**default_statement**       : DEFAULT COLON statement

**loop_statement**          : WHILE LPAREN expr RPAREN statement
                            | DO statement WHILE LPAREN expr RPAREN SEMI
                            | FOR LPAREN expr_statement expr_statement (empty RPAREN) | (expr RPAREN) statement

**init_loop_statement**     : declaration_list | assign_statement | empty

**condition_loop_statement**: factor (EQUAL | NOT_EQUAL | LESS | GRATER | LE_OP | GE_OP) factor | empty

**inc_loop_statement**      : (DEC_OP | INC_OP) variable
                            | variable (INC_OP | DEC_OP)
                            | variable
                            | assign_statement

**assign_statement**        : variable (ASSIGN | PLUS_ASSIGN | MINUS_ASSIGN | MUL_ASSIGN | DIVIDE_ASSIGN | MOD_ASSIGN | XOR_ASSIGN) expr SEMI

**declaration_list**        : type_spec declaration (COMMA declaration)* SEMI

**declaration**             : variable (ASSIGN expr)?

**print_statement**         : COUT LEFT_OP_COUT expr (LEFT_OP_COUT expr)* SEMI

**expr_statement**          : expr SEMI

**expr**                    : ternary_operator

**ternary_operator**        : logical_or (QUESTION_MARK expr COLON ternary_operator)?

**logical_or**              : logical_and (LOG_OR logical_and)*

**logical_and**             : bitwise_or (LOG_AND bitwise_or)*

**bitwise_or**              : bitwise_xor (OR_OP bitwise_xor)*

**bitwise_xor**             : bitwise_and (XOR_OP bitwise_and)*

**bitwise_and**             : equality_ops (AND_OP equality_ops)*

**equality_ops**            : comparison_ops ((EQUAL | NOT_EQUAL) comparison_ops)*

**comparison_ops**          : left_right_ops ((LESS | GRATER | LE_OP | GE_OP) left_right_ops)*

**left_right_ops**          : add_sub_ops ((LEFT_OP | RIGHT_OP) add_sub_ops)*

**add_sub_ops**             : mul_div_mod_ops ((PLUS | MINUS) mul_div_mod_ops)*

**mul_div_mod_ops**         : cast_operator ((MUL | DIV | MOD) cast_operator)*

**cast_operator**           : LPAREN type_spec RPAREN cast_operator
                            | type_spec LPAREN cast_operator RPAREN
                            | unary_operator

**unary_operator**          : INC_OP prefix_operator
                            | DEC_OP prefix_operator
                            | PLUS cast_operator
                            | MINUS cast_operator
                            | LOG_NOT cast_operator
                            | NOT_OP cast_operator
                            | AND_OP cast_operator
                            | postfix_operator

**prefix_operator_rep**     : INC_OP prefix_operator_rep
                            | DEC_OP prefix_operator_rep
                            | variable

**postfix_operator_rep**    : postfix_operator_rep INC_OP 
                            | postfix_operator_rep DEC_OP
                            | variable

**factor**                  : LPAREN expr RPAREN
                            | constant
                            | variable

**constant**                : INTEGER_CONST
                            | FLOAT_CONST
                            | CHAR_CONST
                            | STRING_CONST
                            | TRUE
                            | FALSE

**type_spec**               : INTEGER | FLOAT | DOUBLE | CHAR | BOOL

**variable**                : ID

**empty**                   :
