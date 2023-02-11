**program** : imports main

**imports** :
    USING NAMESPACE variable SEMI
    | SHARP INCLUDE LARROW variable RARROW
    | empty
    
**main** : INTEGER MAIN LBRACE statement_list RBRACE

**statement_list** :
    statement
    | statement SEMI statement_list

**statement** :
    assign_statement
    | declaration_statement
    | if_statement
    | for_statement
    | while_statement
    | switch_statement
    | empty

**type_spec** : INT | FLOAT | DOUBLE | CHAR | BOOL

**assignment_statement** : variable ASSIGN expr

**declaration_statement** : type_spec variable (ASSIGN expr)+

**expr** : term ((PLUS | MINUS) term)* 

**term**: factor ((MUL | DIV) factor)*

**factor** : 
    PLUS factor
    | MINUS factor
    | INT_CONST
    | FLOAT_CONST
    | CHAR_SINGLE_CONST
    | CHAR_MULTI_CONST
    | TRUE
    | FALSE
    | LPAREN expr RPAREN
    | type_spec LPAREN expr RPAREN
    | variable

**empty**:

**variable**: ID
