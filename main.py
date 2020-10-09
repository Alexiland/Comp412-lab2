import os
import error
import sys
# import queue
from scanner import *
from parser import *
from rename_register import *
from allocate_register import *

components = {'MEMOP': ['load', 'store'],
              'LOADI': ['loadI'],
              'ARITHOP': ['add', 'sub', 'mult', 'lshift', 'rshift'],
              'OUTPUT': ['output'],
              'NOP': ['nop'],
              'CONSTANT': [],
              'REGISTER': [],
              'COMMA': [','],
              'INTO': ['=>'],
              'EOF': ['']}

conversion = {0: 'MEMOP',
              1: 'LOADI',
              2: 'ARITHOP',
              3: 'OUTPUT',
              4: 'NOP',
              5: 'CONST',
              6: 'REG',
              7: 'COMMA',
              8: 'INTO',
              9: 'EOF'}

conversion_list = ['MEMOP', 'LOADI', 'ARITHOP', 'OUTPUT', 'NOP', 'CONSTANT', 'REGISTER', 'COMMA', 'INTO', 'EOF']

number_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

err_record = queue.Queue()
have_line_and_message = False


def main():
    global_err = error.Error()
    args = sys.argv
    path = args[-1]
    if not os.path.exists(path):
        global_err.check_error(0)
    if len(args) == 1:
        sys.stdout.write('General format is ./412alloc [flags] filename\n\n'
                         'Default operation is -p')
    elif args[1] == '-h':
        h()
    elif args[1] =='-x':
        scanner = Scanner(path)
        x(scanner)
    elif args[1] =='-d':
        scanner = Scanner(path)
        d(scanner)
    elif is_int(args[1]):
        int_k = int(args[1])
        if 3 <= int_k <= 64:
            scanner = Scanner(path)
            k(int_k, scanner)
        else:
            sys.stderr.write('[ERROR]: expected k in [3,64]\n')
    else:
        global_err.check_error(3)


def h():
    sys.stdout.write(
        'Comp 412 Front End\n\nCommand Syntax:\n\t '
        './412alloc [flags] filename\n\nRequired arguments: '
        '\n\tfilename is a pathname to the input file\n\nOptional flags:\n\t'
        '-h\tprint this message\n\t'
        '-x\tperform register renaming on given input file\n\t')


def x(scanner):
    parser = Parser(scanner)
    result = parser.parse()
    if isinstance(result, IR) and not scanner.error_flag:
        rename_register(result)
        result.traverse()

def k(k, scanner):
    parser = Parser(scanner)
    result = parser.parse()
    if isinstance(result, IR) and not scanner.error_flag:
        rename_register(result)
        allocator = Allocator(result, k)
        allocator.allocate_registers()
        result.traverse()

def d(scanner):
    parser = Parser(scanner)
    result = parser.parse()
    if isinstance(result, IR) and not scanner.error_flag:
        rename_register(result)


def scanner_stdout(line_num, opcode, operation):
    if opcode == 0:
        sys.stdout.write('{}: < MEMOP    , \'{}\' >\n'.format(line_num + 1, operation))
    elif opcode == 1:
        sys.stdout.write('{}: < LOADI    , \'{}\' >\n'.format(line_num + 1, operation))
    elif opcode == 2:
        sys.stdout.write('{}: < ARITHOP  , \'{}\' >\n'.format(line_num + 1, operation))
    elif opcode == 3:
        sys.stdout.write('{}: < OUTPUT   , \'{}\' >\n'.format(line_num + 1, operation))
    elif opcode == 4:
        sys.stdout.write('{}: < NOP      , \'{}\' >\n'.format(line_num + 1, operation))
    elif opcode == 5:
        sys.stdout.write('{}: < CONST    , \'{}\' >\n'.format(line_num + 1, operation))
    elif opcode == 6:
        sys.stdout.write('{}: < REG      , \'{}\' >\n'.format(line_num + 1, operation))
    elif opcode == 7:
        sys.stdout.write('{}: < COMMA    , \'{}\' >\n'.format(line_num + 1, operation))
    elif opcode == 8:
        sys.stdout.write('{}: < INTO     , \'{}\' >\n'.format(line_num + 1, operation))
    elif opcode == 9:
        sys.stdout.write('{}: < ENDFILE  , \'{}\' >\n'.format(line_num + 1, operation))


def scanner_stderr(line_num, word):
    # err_record.put('{}: {} is not a valid word\n'.format(line_num, word))
    sys.stderr.write('---Line------Message\n')
    sys.stderr.write('{}: {} is not a valid word\n'.format(line_num, word))

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def print_error():
    sys.stderr.write('---Line------Message\n')
    while not err_record.empty():
        sys.stderr.write(err_record.get())


if __name__ == '__main__':
    main()
