import Queue as queue
import os
import sys


class Scanner(object):

    def __init__(self, f):
        self.f = open(f, 'r')
        self.char_index = 0
        self.line_index = 0
        # self.line_num = len(self.f)
        self.flag = True
        self.error_flag = False
        self.num_error = 0
        self.line = self.f.readline()
        self.line_error = False


    def __exit__(self):
        self.f.close()

    def next_token(self):
        while self.flag:
            line = self.line
            if line == '':
                break
            max_index = len(line)
            while self.char_index < max_index:
                op = ''
                cat = -1
                # this is the case for EOF
                if line[self.char_index] == '':
                    op = ''
                    cat = 9
                    return Token(self.line_index, cat, op)

                # this is the case for whitespace
                elif line[self.char_index] == ' ':
                    self.char_index = self.char_index + 1

                elif line[self.char_index] == '\n':
                    self.char_index = self.char_index + 1

                elif line[self.char_index] == '\t':
                    self.char_index = self.char_index + 1

                elif line[self.char_index] == ',':
                    op = ','
                    cat = 7
                    self.char_index = self.char_index + 1
                    return Token(self.line_index, cat, op)

                # this is for comments
                elif line[self.char_index] == '/' and self.char_index < max_index - 1:
                    if line[self.char_index + 1] == '/':
                        self.char_index = max_index
                    else:
                        self.char_index = self.char_index + 1
                        op = '/'
                        self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                          self.char_index, op)
                        break

                # this is for =>
                elif line[self.char_index] == '=' and self.char_index < max_index - 1:
                    if line[self.char_index + 1] == '>':
                        op = '=>'
                        cat = 8
                        self.char_index = self.char_index + 2
                        return Token(self.line_index, cat, op)
                    else:
                        self.char_index = self.char_index + 1
                        op = '='
                        self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                          self.char_index, op)
                        break



                # this is the case for 'add'
                elif line[self.char_index] == 'a' and self.char_index < max_index - 2:
                    if line[self.char_index + 1] == 'd':
                        # this checks if the next character immediately after the last character of op is a separate character, if no, then it is not a valid op code
                        if line[self.char_index + 2] == 'd' and (
                                self.char_index + 2 == max_index - 1 or line[self.char_index + 3] == ' ' or line[
                            self.char_index + 3] == ',' or line[self.char_index + 3] == '\n' or line[
                                    self.char_index + 3] == '\t' or line[self.char_index + 3] == '/'):
                            op = 'add'
                            cat = 2
                            self.char_index = self.char_index + 3
                            return Token(self.line_index, cat, op)
                        else:
                            self.char_index = self.char_index + 2
                            op = 'ad'
                            # if the third character is not 'd', then it is not one of the operation
                            self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                              self.char_index, op)
                            break
                    else:
                        self.char_index = self.char_index + 1
                        op = 'a'
                        # if the third character is not 'd', then it is not one of the operation
                        self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                          self.char_index, op)
                        break

                # this is for 'nop'
                elif line[self.char_index] == 'n' and self.char_index < max_index - 2:
                    if line[self.char_index + 1] == 'o':
                        if line[self.char_index + 2] == 'p' and (
                                self.char_index + 2 == max_index - 1 or line[self.char_index + 3] == ' ' or line[
                            self.char_index + 3] == ',' or line[
                                    self.char_index + 3] == '\n' or line[self.char_index + 3] == '\t' or line[
                                    self.char_index + 3] == '/'):
                            op = 'nop'
                            cat = 4
                            self.char_index = self.char_index + 3
                            return Token(self.line_index, cat, op)
                        else:
                            self.char_index = self.char_index + 2
                            op = 'no'
                            # if the third character is not 'd', then it is not one of the operation
                            self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                              self.char_index, op)
                            break

                    else:
                        self.char_index = self.char_index + 1
                        op = 'n'
                        # if the third character is not 'd', then it is not one of the operation
                        self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                          self.char_index, op)
                        break

                # this is for 'output'
                elif line[self.char_index] == 'o' and self.char_index < max_index - 5:
                    if line[self.char_index + 1] == 'u':
                        if line[self.char_index + 2] == 't':
                            if line[self.char_index + 3] == 'p':
                                if line[self.char_index + 4] == 'u':
                                    if line[self.char_index + 5] == 't' and (
                                            self.char_index + 5 == max_index - 1 or line[self.char_index + 6] == ' ' or
                                            line[self.char_index + 6] == ',' or line[
                                                self.char_index + 6] == '\n' or line[self.char_index + 6] == '\t' or
                                            line[self.char_index + 6] == '/'):
                                        op = 'output'
                                        cat = 3
                                        self.char_index = self.char_index + 6
                                        return Token(self.line_index, cat, op)
                                    else:
                                        self.char_index = self.char_index + 5
                                        op = 'outpu'
                                        self.char_index = self.loop_nonexistent_operation(max_index, line,
                                                                                          self.line_index,
                                                                                          self.char_index, op)
                                        break
                                else:
                                    self.char_index = self.char_index + 4
                                    op = 'outp'
                                    self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                                      self.char_index, op)
                                    break
                            else:
                                self.char_index = self.char_index + 3
                                op = 'out'
                                self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                                  self.char_index, op)
                                break
                        else:
                            self.char_index = self.char_index + 2
                            op = 'ou'
                            self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                              self.char_index, op)
                            break
                    else:
                        self.char_index = self.char_index + 1
                        op = 'o'
                        self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                          self.char_index, op)
                        break

                # this is for sub/store
                elif line[self.char_index] == 's' and self.char_index < max_index - 2:
                    if line[self.char_index + 1] == 't' and self.char_index < max_index - 4:
                        if line[self.char_index + 2] == 'o':
                            if line[self.char_index + 3] == 'r':
                                if line[self.char_index + 4] == 'e' and (
                                        self.char_index + 4 == max_index - 1 or line[self.char_index + 5] == ' ' or
                                        line[self.char_index + 5] == ',' or line[
                                            self.char_index + 5] == '\n' or line[self.char_index + 5] == '\t' or line[
                                            self.char_index + 5] == '/'):
                                    op = 'store'
                                    cat = 0
                                    self.char_index = self.char_index + 5
                                    return Token(self.line_index, cat, op)
                                else:
                                    self.char_index = self.char_index + 4
                                    op = 'stor'

                                    self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                                      self.char_index, op)
                                    break
                            else:
                                self.char_index = self.char_index + 3
                                op = 'sto'
                                self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                                  self.char_index, op)
                                break
                        else:
                            self.char_index = self.char_index + 2
                            op = 'st'
                            self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                              self.char_index, op)
                            break
                    elif line[self.char_index + 1] == 'u':
                        if line[self.char_index + 2] == 'b' and (
                                self.char_index + 2 == max_index - 1 or line[self.char_index + 3] == ' ' or line[
                            self.char_index + 3] == ',' or line[
                                    self.char_index + 3] == '\n' or line[self.char_index + 3] == '/' or line[
                                    self.char_index + 3] == '\t'):
                            op = 'sub'
                            cat = 2
                            self.char_index = self.char_index + 3
                            return Token(self.line_index, cat, op)
                        else:
                            self.char_index = self.char_index + 2
                            op = 'su'
                            self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                              self.char_index, op)
                            break
                    else:
                        self.char_index = self.char_index + 1
                        op = 's'
                        self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                          self.char_index, op)
                        break

                # this is for loadI
                elif line[self.char_index] == 'l' and self.char_index < max_index - 3:
                    if line[self.char_index + 1] == 'o':
                        if line[self.char_index + 2] == 'a':
                            if line[self.char_index + 3] == 'd' and self.char_index < max_index - 4:
                                if line[self.char_index + 4] == 'I' and (
                                        self.char_index + 4 == max_index - 1 or line[self.char_index + 5] == ' ' or
                                        line[self.char_index + 5] == ',' or line[
                                            self.char_index + 5] == '\n' or line[self.char_index + 5] == '\t' or line[
                                            self.char_index + 5] == '/'):
                                    self.char_index = self.char_index + 5
                                    op = 'loadI'
                                    cat = 1
                                    return Token(self.line_index, cat, op)
                                elif (self.char_index + 3 == max_index - 1 or line[self.char_index + 4] == ' ' or line[
                                    self.char_index + 4] == ',' or line[
                                          self.char_index + 4] == '\n' or line[self.char_index + 4] == '\t' or line[
                                          self.char_index + 4] == '/'):
                                    self.char_index = self.char_index + 4
                                    op = 'load'
                                    cat = 0
                                    return Token(self.line_index, cat, op)
                                else:
                                    self.char_index = self.char_index + 4
                                    op = 'load'
                                    self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                                      self.char_index, op)
                                    break
                            elif line[self.char_index + 3] == 'd' and (
                                    self.char_index + 3 == max_index - 1 or line[self.char_index + 4] == ' ' or line[
                                self.char_index + 4] == ',' or line[
                                        self.char_index + 4] == '\n' or line[self.char_index + 4] == '\t'):
                                self.char_index = self.char_index + 4
                                op = 'load'
                                cat = 0
                                return Token(self.line_index, cat, op)
                            else:
                                self.char_index = self.char_index + 3
                                op = 'loa'
                                self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                                  self.char_index, op)
                                break
                        else:
                            self.char_index = self.char_index + 2
                            op = 'lo'
                            self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                              self.char_index, op)
                            break
                    elif line[self.char_index + 1] == 's' and self.char_index < max_index - 5:
                        if line[self.char_index + 2] == 'h':
                            if line[self.char_index + 3] == 'i':
                                if line[self.char_index + 4] == 'f':
                                    if line[self.char_index + 5] == 't' and (
                                            self.char_index + 5 == max_index - 1 or line[self.char_index + 6] == ' ' or
                                            line[self.char_index + 6] == ',' or line[
                                                self.char_index + 6] == '\n' or line[self.char_index + 6] == '\t' or
                                            line[self.char_index + 6] == '/'):
                                        self.char_index = self.char_index + 6
                                        op = 'lshift'
                                        cat = 2
                                        return Token(self.line_index, cat, op)
                                    else:
                                        self.char_index = self.char_index + 5
                                        op = 'lshif'
                                        self.char_index = self.loop_nonexistent_operation(max_index, line,
                                                                                          self.line_index,
                                                                                          self.char_index, op)
                                        break
                                else:
                                    self.char_index = self.char_index + 4
                                    op = 'lshi'
                                    self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                                      self.char_index, op)
                                    break
                            else:
                                self.char_index = self.char_index + 3
                                op = 'lsh'
                                self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                                  self.char_index, op)
                                break
                        else:
                            self.char_index = self.char_index + 2
                            op = 'ls'
                            self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                              self.char_index, op)
                            break
                    else:
                        self.char_index = self.char_index + 1
                        op = 'l'
                        self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                          self.char_index, op)
                        break

                # this is for 'rshift'
                elif line[self.char_index] == 'r' and self.char_index < max_index - 1:
                    op = line[self.char_index]
                    if line[self.char_index + 1] == 's' and self.char_index < max_index - 5:
                        if line[self.char_index + 2] == 'h':
                            if line[self.char_index + 3] == 'i':
                                if line[self.char_index + 4] == 'f':
                                    if line[self.char_index + 5] == 't' and (
                                            self.char_index + 5 == max_index - 1 or line[self.char_index + 6] == ' ' or
                                            line[self.char_index + 6] == ',' or line[
                                                self.char_index + 6] == '\n' or line[self.char_index + 6] == '\t' or
                                            line[self.char_index + 6] == '/'):
                                        self.char_index = self.char_index + 6
                                        op = 'rshift'
                                        cat = 2
                                        return Token(self.line_index, cat, op)
                                    else:
                                        self.char_index = self.char_index + 5
                                        op = 'rshif'
                                        self.char_index = self.loop_nonexistent_operation(max_index, line,
                                                                                          self.line_index,
                                                                                          self.char_index, op)
                                        break
                                else:
                                    self.char_index = self.char_index + 4
                                    op = 'rshi'
                                    self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                                      self.char_index, op)
                                    break
                            else:
                                self.char_index = self.char_index + 3
                                op = 'rsh'
                                self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                                  self.char_index, op)
                                break
                        else:
                            self.char_index = self.char_index + 2
                            op = 'rs'
                            self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                              self.char_index, op)
                            break
                    elif '0' <= line[self.char_index + 1] <= '9':
                        while not self.char_index == max_index - 1 and '0' <= line[self.char_index + 1] <= '9':
                            self.char_index += 1
                            op += line[self.char_index]
                        # if self.char_index == max_index - 1 or line[self.char_index + 1] == ' ' or line[
                        #     self.char_index + 1] == ',' or line[self.char_index + 1] == '\n' or \
                        #         line[self.char_index + 1] == '\t' or line[self.char_index + 1] == '/':
                        #     cat = 6
                        #     self.char_index = self.char_index + 1
                        #     return Token(self.line_index, cat, op)
                        if self.char_index == max_index - 1 or not ('0' <= line[self.char_index + 1] <= '9'):
                            cat = 6
                            self.char_index = self.char_index + 1
                            return Token(self.line_index, cat, op)
                        else:
                            self.char_index += 1
                            self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                              self.char_index, op)
                            break

                    else:
                        self.char_index = self.char_index + 1
                        self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                          self.char_index, op)
                        break

                # this is for mult
                elif line[self.char_index] == 'm' and self.char_index < max_index - 3:
                    if line[self.char_index + 1] == 'u':
                        if line[self.char_index + 2] == 'l':
                            if line[self.char_index + 3] == 't' and (
                                    self.char_index + 3 == max_index - 1 or line[self.char_index + 4] == ' ' or line[
                                self.char_index + 4] == ',' or
                                    line[
                                        self.char_index + 4] == '\n' or line[self.char_index + 4] == '/' or line[
                                        self.char_index + 4] == '\t'):
                                self.char_index = self.char_index + 4
                                op = 'mult'
                                cat = 2
                                return Token(self.line_index, cat, op)
                            else:
                                self.char_index = self.char_index + 3
                                op = 'mul'
                                self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                                  self.char_index, op)
                                break
                        else:
                            self.char_index = self.char_index + 2
                            op = 'mu'
                            self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                              self.char_index, op)
                            break
                    else:
                        self.char_index = self.char_index + 1
                        op = 'm'
                        self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                          self.char_index, op)
                        break

                # this is for unsigned integer
                elif '0' <= line[self.char_index] <= '9':
                    op = line[self.char_index]
                    while not self.char_index == max_index - 1 and '0' <= line[self.char_index + 1] <= '9':
                        op += line[self.char_index + 1]
                        self.char_index += 1
                    # if self.char_index == max_index - 1 or line[self.char_index + 1] == ' ' or line[
                    #     self.char_index + 1] == ',' or line[self.char_index + 1] == '\n' or line[
                    #     self.char_index + 1] == '\t' or line[self.char_index + 1] == '/':
                    #     cat = 5
                    #     self.char_index = self.char_index + 1
                    #     return Token(self.line_index, cat, op)
                    if self.char_index == max_index - 1 or not ('0' <= line[self.char_index + 1] <= '9'):
                        cat = 5
                        self.char_index = self.char_index + 1
                        return Token(self.line_index, cat, op)
                    else:
                        while not (self.char_index == max_index - 1 or line[self.char_index] == ' ' or line[
                            self.char_index] == '\n' or line[self.char_index] == ',' or line[
                                       self.char_index] == '\t' or line[self.char_index] == '/'):
                            op += line[self.char_index + 1]
                            self.char_index += 1
                        self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index,
                                                                          self.char_index, op)
                        break

                else:
                    self.char_index = self.loop_nonexistent_operation(max_index, line, self.line_index, self.char_index,
                                                                      '')
                    self.char_index += 1
                    break

            self.char_index = 0
            self.line_index += 1
            self.line = self.f.readline()

        return Token(self.line_index - 1, 9, '')

    def loop_nonexistent_operation(self, max_index, line, line_idx, i, op):
        index = i
        self.error_flag = True
        self.num_error += 1

        while index < max_index and not line[index] == '\n' and not line[index] == ' ' and not line[
                                                                                                   index] == ',' and not \
                line[index] == '\t':
            # we append the wrong-spelling operation to errors
            op = op + line[index]
            index = index + 1
        self.line_error = True

        self.scanner_stderr(line_idx + 1, op)
        return index

    def next_line(self):
        self.line = self.f.next()
        self.char_index = 0

    def scanner_stderr(self, line_num, word):
        # self.err_record.put('{}: {} is not a valid word\n'.format(line_num, word))
        # if not self.error_flag:
        #     sys.stderr.write("                         \n")
        #     sys.stderr.write("Line       Message       \n")
        #     sys.stderr.write("-------------------------\n")
        #     self.error_flag = True
        sys.stderr.write('{}: "{}" is not a valid word\n'.format(line_num, word))


class Token(object):
    def __init__(self, line_num, opcode, lexeme):
        self.line_num = line_num + 1
        self.lexeme = lexeme
        self.opcode = opcode

        if opcode == 0:
            self.category = 'MEMOP'
        elif opcode == 1:
            self.category = 'LOADI'
        elif opcode == 2:
            self.category = 'ARITHOP'
        elif opcode == 3:
            self.category = 'OUTPUT'
        elif opcode == 4:
            self.category = 'NOP'
        elif opcode == 5:
            self.category = 'CONST'
        elif opcode == 6:
            self.category = 'REG'
        elif opcode == 7:
            self.category = 'COMMA'
        elif opcode == 8:
            self.category = 'INTO'
        elif opcode == 9:
            self.category = 'ENDFILE'
        else:
            self.category = 'ERROR'

    def __str__(self):
        # return '{}: < {}  , \'{}\' >\n'.format(self.line_num, self.category, self.lexeme)
        if self.opcode == 0:
            return '{}: < MEMOP    , \'{}\' >\n'.format(self.line_num, self.lexeme)
        elif self.opcode == 1:
            return '{}: < LOADI    , \'{}\' >\n'.format(self.line_num, self.lexeme)
        elif self.opcode == 2:
            return '{}: < ARITHOP  , \'{}\' >\n'.format(self.line_num, self.lexeme)
        elif self.opcode == 3:
            return '{}: < OUTPUT   , \'{}\' >\n'.format(self.line_num, self.lexeme)
        elif self.opcode == 4:
            return '{}: < NOP      , \'{}\' >\n'.format(self.line_num, self.lexeme)
        elif self.opcode == 5:
            return '{}: < CONST    , \'{}\' >\n'.format(self.line_num, self.lexeme)
        elif self.opcode == 6:
            return '{}: < REG      , \'{}\' >\n'.format(self.line_num, self.lexeme)
        elif self.opcode == 7:
            return '{}: < COMMA    , \'{}\' >\n'.format(self.line_num, self.lexeme)
        elif self.opcode == 8:
            return '{}: < INTO     , \'{}\' >\n'.format(self.line_num, self.lexeme)
        elif self.opcode == 9:
            return '{}: < ENDFILE  , \'{}\' >\n'.format(self.line_num, self.lexeme)
