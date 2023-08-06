parser grammar fcssParser;

options {
    tokenVocab=fcssLexer;
}

// Trees
tree
    : (assign_stmt | append_stmt | conditional_block | switch)*
    ;

main_tree
    : selector
    ;

// Basic atoms/expressions

attribute
    : IDENTIFIER ('.' IDENTIFIER)*
    ;

// TODO: Write param spec for passing parameters in functions
function_call
    : attribute '(' ')'
    ;

atom
    : attribute
    | function_call
    | NULL
    | INTEGRAL
    | DOUBLE
    | BOOLEAN
    | STRING
    ;

expr
    : unary_left=('+'|'-'|'_'|'^'|'!') right=expr
    | left=expr op='**' right=expr
    | left=expr op=('*'|'/'|'%') right=expr
    | left=expr op=('+'|'-') right=expr
    | left=expr op=('>='|'>') right=expr
    | left=expr op=('<='|'<') right=expr
    | left=expr op=('=='|'!=') right=expr
    | left=expr op=('||'|'&&') right=expr
    | atom
    | '(' atom ')'
    | '(' expr ')'
    ;

// Statements

assign_stmt
    : attribute '=' expr ';'
    ;

append_stmt
    : attribute op=('+='|'-='|'*='|'/='|'**='|'%=') expr ';'
    ;

if_stmt
    : 'if' expr '{' tree '}'
    | 'if' '(' expr ')' '{' tree '}'
    ;

else_if_stmt
    : 'else if' expr '{' tree '}'
    | 'else if' '(' expr ')' '{' tree '}'
    ;

else_stmt
    : 'else' '{' tree '}'
    ;

conditional_block
    : if_stmt (else_if_stmt)* (else_stmt)?
    ;


// Selectors/Functions

selector_name
    : token=('.'|'#') IDENTIFIER
    | IDENTIFIER
    | wildcard=('*'|'**')
    ;

selector_pattern
    : selector_name operand='||' selector_name
    | selector_name operand='&&' selector_name
    | unary='!' selector_name
    | unary='!' '(' selector_name ')'
    | selector_name
    ;

selector
    : ('[' selector_pattern+ ']')+ '{' tree '}'
    | ('[' selector_pattern+ ']')+ '.' IDENTIFIER '{' tree '}'
    ;

// Switch Case?
switch
    : 'switch' expr '{' (case)*? '}'
    | 'switch' '(' expr ')' '{' (case)*? '}'
    ;

case
    : 'case' expr '{' tree '}'
    | 'case' '(' expr ')' '{' tree '}'
    ;
