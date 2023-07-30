parser grammar fcssParser;

options {
    tokenVocab=fcssLexer;
}

attr
    : NAME ('.' NAME)+
    ;

name_or_attr
    : attr | NAME
    ;

// Statements

assign_stmt
    : name_or_attr EQUALS expr
    ;

// Selectors

selector_type
    : '#'
    | '.'
    ;

selector
    : ('[' selector_type? NAME ']')+
    | ('[*]')+
    | ('[**]')+
    ;

selector_meth
    : selector '.' NAME
    | selector '.' NAME parameters
    ;

// Style Defs

generic_style
    : selector_meth OPEN_BRACE CLOSE_BRACE
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
    : 'null'
    | BOOLEAN
    | INTEGER
    | DOUBLE
    | STRING
    | '('? atoms ')'?
    ;

expr
    : expr '**' expr
    | ('+'|'-'|'_'|'^'|'!') '('? expr ')'?
    | expr ('*'|'/'|'%') expr
    | expr ('+'|'-') expr
    | expr ('>'|'>='|'<'|'<='|'!='|'==') expr
    | atoms
    ;
