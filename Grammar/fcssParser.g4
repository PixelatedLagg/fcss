parser grammar fcssParser;

options {
    tokenVocab=fcssLexer;
}

// Trees
tree
    : (assign_stmt | append_stmt | conditional_block | selector)*
    ;

// Basic atoms/expressions

attribute
    : IDENTIFIER ('.' IDENTIFIER)*
    ;

// TODO: Write param spec for passing parameters in functions
param_spec
    : ((atom)*? (',' (atom)*?)+ (',')?)
    ;

function_call
    : attribute '(' param_spec ')'
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

selector
    : '[' selector_name ']' '{' tree '}'
    | '[' selector_name ']' '.' IDENTIFIER '{' tree '}'
    ;
