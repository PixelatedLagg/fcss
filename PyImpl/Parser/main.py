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
    help='Input file to parse', nargs=1, metavar='*I...',
)

parser.add_argument(
    '--O', '-output', type=str, dest='output', default='?output.json',
    help='File to output results to', required=False, metavar='*Path'
)

parser.add_argument(
    '--F', '-format', type=str, choices=('json',), dest='format',
    help='Format to save file as', required=False
)

parser.add_argument(
    '--C', '-compress', action='store_true', default=False, dest='compress',
    help='Compresses the parsed file to take up less space', required=False
)

parser.add_argument(
    '--BP', '--browser-parsing', action='store_true', default=True, dest='bp',
    help='Whether file is being processed for browsers, supresses local filesystem errors',
    required=False
)

parser.add_argument(
    '--DP', '-default-path', type=str, default='?', dest='dp',
    help='Path pointing to were fcss files are found, defaults to current file directory or `/` for [BP]',
    required=False, metavar='*Path'
)

if __name__ == '__main__':
    v = parser.parse_args(argv[1:])
    d = vars(v)

    if d['output'].startswith('?') and d['compress']:
        d['output'] = d['output'].split('.')[0][1:] + '.Zlib'
    elif d['output'].startswith('?'):
        d['output'] = d['output'][1:]

    if d['dp'].startswith('?'):
        if d['bp']:
            d['dp'] = '/' + d['dp'][1:]
        else:
            d['dp'] = d['dp'][1:]
    
    stream = InputStream(d['input'][0].read())
    lexer = fcssLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = fcssParser(token_stream)

    visitor = fcssVisitor(d['input'][0].name, d['bp'])
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
