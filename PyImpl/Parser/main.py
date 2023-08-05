from antlr4 import *
from libs.fcssLexer import fcssLexer
from libs.fcssParser import fcssParser
from visitor import fcssVisitor
from pprint import pprint

## Do need to rewrite this for CLI handling later
code = """
// Sets width of element to 90% of the screen
// If its the last element in the selector adds a bottom border with width=3

[div][#my_class] {
    width = Screen.width * .90;
    if (this.last()) {
        border.bottom += 3;
    }
}
"""

stream = InputStream(code)
lexer = fcssLexer(stream)
token_stream = CommonTokenStream(lexer)
parser = fcssParser(token_stream)
tree = parser.tree()
visitor = fcssVisitor()

pprint(visitor.visit(tree), indent=4, sort_dicts=False)
