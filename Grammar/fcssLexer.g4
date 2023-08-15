lexer grammar fcssLexer;

// Keywords
TRUE:       'true';
FALSE:      'false';
IF:         'if';
ELSEIF:     'else if';
ELSE:       'else';
NULL:       'null';
SWITCH:     'switch';
CASE:       'case';
WHILE:      'while';
IMPORT:     'import';

IDENTIFIER
    : [a-zA-Z_]([a-zA-Z0-9_-])*([a-zA-Z0-9_])*
    ;

// Data Types

INTEGRAL
    : [0-9]+
    ;

BOOLEAN
    : TRUE
    | FALSE
    ;

DOUBLE
    : INTEGRAL '.'
    | INTEGRAL '.' INTEGRAL
    | '.' INTEGRAL
    ;

STRING
    : '\'' (~[\\\n\r\f])* '\''
    | '"' (~[\\\n\r\f])* '"'
    ;

// Symbols
DOT:            '.';
COMMA:          ',';
SEMI_COLON:     ';';
ASSIGN:         '=';
HASHTAG:        '#';    // Token for defining classes

OPEN_PAREN:     '(';
CLOSE_PAREN:    ')';
OPEN_BRACK:     '[';
CLOSE_BRACK:    ']';
OPEN_BRACE:     '{';
CLOSE_BRACE:    '}';

// Operations

ADD_OP:         '+';
SUB_OP:         '-';
MUL_OP:         '*';
DIV_OP:         '/';
POW_OP:         '**';
MOD_OP:         '%';
FLOOR_OP:       '_';
CEIL_OP:        '^';

// Appendable Ops
AP_ADD_OP:      '+=';
AP_SUB_OP:      '-=';
AP_MUL_IP:      '*=';
AP_DIV_OP:      '/=';
AP_POW_OP:      '**=';
AP_MOD_OP:      '%=';

// Comparity Operations

GREATER:        '>';
GREATER_EQUAL:  '>=';
LESS:           '<';
LESS_EQUAL:     '<=';
EQUALS:         '==';
NOT_EQUALS:     '!=';

// Boolean Operators
AND:            '&&';
OR:             '||';
NOT:            '!';

// Comments
COMMENT:        '//' ~[\n\r\f]* -> skip;

// Elements to skip
WS:             [ \n\t\r]+ -> skip;
