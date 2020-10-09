import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='412alloc')
    # parser.add_argument('-h', help='help option', action='store_true')
    parser.add_argument('-s', default=None, type=str,
                        help='read the file specified by <file name> and print, '
                             'to the standard output stream, '
                             'a list of the tokens that the scanner found')
    parser.add_argument('-p', '-parse', default=None, type=str,
                        help='read the file specified by <file name>, '
                             'scan it and parse it, build the intermediate '
                             'representation, and report either success or '
                             'report all of the errors that it finds in the input file')
    parser.add_argument('-r', '-read', default=None, type=str,
                        help=' read the file specified by <file name>, '
                             'scan it, parse it, build the intermediate representation, '
                             'and print out the information in the intermediate representation ('
                             'in an appropriately human readable format)')
    args = parser.parse_args()
    return args
