/* Creates the antlr lexer and parser files needed to compile fcss files,
relies on the python `antlr4-python-runtime` lib.

First we need to generate our lexer, so the parser can use the tokens
`antlr4 -o ./path/to/Compiler/.antlr -Dlanguage=Cpp ./path/to/Grammar/fcssLexer.g4`

After we have our lexer, we can make our parser
`antlr4 -o ./path/to/Compiler/.antlr -Dlanguage=Cpp ./path/to/Grammar/fcssParser.g4`

By default we will search for our lexer and parser class in `Compiler/.antlr`
*/
