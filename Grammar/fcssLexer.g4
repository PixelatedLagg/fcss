lexer grammar fcssLexer;

NAME
    : [a-zA-Z_]
    : [a-zA-Z_][a-zA-Z0-9_-]*[a-zA-Z0-9_]*
    ;

// Kw
TRUE:           'true';
FALSE:          'false';
IF:             'if';
ELSE:           'else';
ELSE_IF:        'else if';

INTEGER
    : [1-9] INTEGRAL*
    | '0'+
    ;

STRING
    : SINGLE_STRING
    | DOUBLE_STRING
    ;

DOUBLE
    : INTEGRAL? FRACTION
    | INTEGRAL '.'
    ;

BOOLEAN
    : TRUE
    | FALSE
    ;

// Symbols

DOT:            '.';
COMMA:          ',';
SEMI_COLON      ';';
ASSIGN:         '=';

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

// Fragments

fragment SINGLE_STRING
    : '\'' ( ~[\\\r\n\f'] )* '\''
    ;

fragment DOUBLE_STRING
    : '"' ( ~[\\\r\n\f"] )* '"'
    ;

// Numbers

fragment DIGIT
    : [0-9]
    ;

fragment INTEGRAL
    : DIGIT+
    ;

fragment FRACTION
    : '.' INTEGRAL
    ;

// Ignorable elements

fragment SPACES
    : [ \t]+
    ;

fragment COMMENT
    : '//' ~[\r\n\f]*
    ;
