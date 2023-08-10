from antlr4 import InputStream, CommonTokenStream
from libs.fcssLexer import fcssLexer
from libs.fcssParser import fcssParser
from visitor import fcssVisitor
from json import dumps
from zlib import compress
import argparse
from sys import argv

parser = argparse.ArgumentParser(
    prog='fcssParser',
    description='Processes a .fcss file transforming it into an executable instruction set',
)

parser.add_argument(
    'input', type=argparse.FileType(encoding='utf-8'),
    help='Input file to parse', nargs=1, metavar='I'
)

parser.add_argument(
    '--O', '-output', type=str, dest='output', default='?output.json',
    help='File to output results to', required=False
)

parser.add_argument(
    '--F', '-format', type=str, choices=('json',), dest='format',
    help='Format to save file as', required=False
)

parser.add_argument(
    '--C', '-compress', action='store_true', default=False, dest='compress',
    help='Compresses the parsed file to take up less space', required=False
)

if __name__ == '__main__':
    v = parser.parse_args(argv[1:])
    d = vars(v)

    if not (d['input'] or d['output']):
        parser.print_help()
        exit(0)
    
    if d['output'].startswith('?') and d['compress']:
        d['output'] = d['output'].split('.')[0][1:] + '.Zlib'
    elif d['output'].startswith('?'):
        d['output'] = d['output'][1:]

    if not d['input']:
        print('Error: No input file provided')
        exit(1)
    
    stream = InputStream(d['input'][0].read())
    lexer = fcssLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = fcssParser(token_stream)

    visitor = fcssVisitor()
    tree = parser.main_tree()
    r = visitor.visit(tree)

    if d['compress']:
        with open(d['output'], 'wb') as fp:
            compressed_data = dumps(r).encode()
            fp.write(compress(compressed_data))
    else:
        with open(d['output'], 'w') as fp:
            fp.write(dumps(r, indent=4))

    print('Saved output to:', d['output'])
