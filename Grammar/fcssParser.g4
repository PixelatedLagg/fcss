parser grammar fcssParser;

options {
    tokenVocab=fcssLexer;
}

// Trees
tree
    : (assign_stmt | append_stmt | conditional_block | switch_stmt | while_stmt | return_stmt)*
    ;

main_tree
    : (import_stmt | selector_stmt | function_stmt)*
    ;

// Basic atoms/expressions
attribute
    : IDENTIFIER ('.' IDENTIFIER)*
    ;

// Supports function called and left recursive methods which allow for more flexibility
// x.y().z -> OK
extended_attribute
    : extended_attribute ('.' extended_attribute)+
    | extended_attribute '(' ')'
    | extended_attribute '(' expr (',' expr)*? ')'
    | attribute
    ;

atom
    : extended_attribute
    | NULL
    | INTEGRAL
    | DOUBLE
    | 'true'
    | 'false'
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

import_stmt
    : 'import' STRING ';'
    ;

return_stmt
    : 'return' expr ';'
    ;

// Conditionals 

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

// Switch Case?
switch_stmt
    : 'switch' expr '{' (case_stmt)*? '}'
    | 'switch' '(' expr ')' '{' (case_stmt)*? '}'
    ;

case_stmt
    : 'case' (expr)? '{' tree '}'
    | 'case' '(' (expr)? ')' '{' tree '}'
    ;

// Loops

while_stmt
    : 'while' expr '{' tree '}'
    | 'while' '(' expr ')' '{' tree '}'
    ;

// Selectors/Functions

selector_name
    : token=('.'|'#') IDENTIFIER
    | IDENTIFIER
    | wildcard=('*'|'**')
    ;

selector_pattern
    : selector_pattern (operand='||' selector_pattern)+
    | selector_pattern (operand='&&' selector_pattern)+
    | unary='!' selector_pattern
    | unary='!' '(' selector_pattern ')'
    | selector_name
    | '(' selector_name ')'
    | '(' selector_pattern ')'
    ;

selector_stmt
    : ('[' selector_pattern+ ']')+ '{' tree '}'
    | ('[' selector_pattern+ ']')+ '.' IDENTIFIER '{' tree '}'
    ;

// Functions

function_tree
    : tree
    ;

function_stmt
    : 'function' IDENTIFIER '(' ')' '{' function_tree '}'
    | 'function' IDENTIFIER '(' IDENTIFIER (',' IDENTIFIER)* ')' '{' function_tree '}'
    ;
