parser grammar fcssParser;

options {
    tokenVocab=fcssLexer;
}

// Prog - Defines how code in the file may be written
prog
    : generic_style
    ;


attr
    : NAME ('.' NAME)+
    ;

name_or_attr
    : attr | NAME
    ;

// Statements

assign_stmt
    : name_or_attr '=' expr ';'
    ;

if_stmt
    : 'if' expr '{' block '}'
    | 'if' '(' expr ')' '{' block '}'
    ;

else_if_stmt
    : 'else if' expr '{' block '}'
    | 'else if' expr '{' block '}'
    ;

else_stmt
    : 'else' '{' block '}'
    ;

if_else_block
    : if_stmt (else_if_stmt)*? (else_stmt)?
    ;

block
    : assign_stmt
    | if_else_block
    ;

// Selectors

selector_type
    : '#'
    | '.'
    ;

selector
    : ('[' selector_type? NAME ']')+
    | ('[' '*' ']')+
    | ('[' '*' '*' ']')+
    ;

selector_meth
    : selector '.' NAME
    | selector '.' NAME parameters
    | selector
    ;

// Style Defs

generic_style
    : selector_meth '{' block '}'
    ;

// Function Parameters
parameters
    : '(' param_spec ')'
    ;

argslist
    : (NAME ',')+ NAME?
    ;

param_spec
    : NAME
    | argslist
    ;

passable_arglist
    : argslist
    ;

// Expressions

atoms
    : NULL
    | BOOLEAN
    | INTEGER
    | DOUBLE
    | STRING
    | name_or_attr
    ;

expr
    : expr '**' expr
    | ('+'|'-'|'_'|'^'|'!') '('? expr ')'?
    | expr ('*'|'/'|'%') expr
    | expr ('+'|'-') expr
    | expr ('>'|'>='|'<'|'<='|'!='|'==') expr
    | atoms
    | '(' atoms ')'
    ;
