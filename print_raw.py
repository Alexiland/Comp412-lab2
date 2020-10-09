import sys

with open(sys.argv[1], 'r') as f:
    for char in f.read():
        print(repr(char))