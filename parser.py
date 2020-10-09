from scanner import *
from internal_representation import *

class Parser(object):
    def __init__(self, scanner):
        self.scanner = scanner
        self.error = False
        self.list = IR()
        self.num_error = 0
        self.current_line = 0
        self.next_flag = False
        self.word = None

    def parse(self):
        self.word = self.scanner.next_token()
        self.current_line = self.word.line_num

        while not self.word.opcode == 9:

            self.current_line = self.word.line_num
            if self.word.opcode == 0:
                self.finish_memop()
            elif self.word.opcode == 1:
                self.finish_loadI()
            elif self.word.opcode == 2:
                self.finish_arithop()
            elif self.word.opcode == 3:
                self.finish_output()
            elif self.word.opcode == 4:
                self.finish_nop()
            else:
                self.error = True
                self.num_error += 1
                sys.stderr.write(
                    '{}: Operation starts with an invalid opcode: "{}".\n'.format(self.word.line_num, self.word.lexeme))
            if self.next_flag:
                self.next_flag = False
            else:
                self.word = self.scanner.next_token()
        if not self.error:
            return self.list
        else:
            return None

    def finish_memop(self):

        if self.scanner.line_error:
            self.scanner.line_error = False
            self.next_flag = True
            return
        lexeme = self.word.lexeme
        self.word = self.scanner.next_token()
        if (not self.word.opcode == 6 and self.current_line == self.word.line_num) or not self.current_line == self.word.line_num:
            self.error = True
            self.num_error += 1
            sys.stderr.write('{}: Missing source register in load or store.\n'.format(self.current_line))
            self.scanner.char_index = len(self.scanner.line)
        else:
            if self.scanner.line_error:
                self.scanner.line_error = False
                self.next_flag = True
                return
            sour_reg = int(self.word.lexeme[1:])
            self.word = self.scanner.next_token()
            if (not self.word.opcode == 8 and self.current_line == self.word.line_num) or not self.current_line == self.word.line_num:
                self.error = True
                self.num_error += 1
                sys.stderr.write('{}: Missing "=>" in load or store.\n'.format(self.current_line))
                self.scanner.char_index = len(self.scanner.line)
            else:
                if self.scanner.line_error:
                    self.scanner.line_error = False
                    self.next_flag = True
                    return
                self.word = self.scanner.next_token()
                if (not self.word.opcode == 6 and self.current_line == self.word.line_num) or not self.current_line == self.word.line_num:
                    self.error = True
                    self.num_error += 1
                    sys.stderr.write('{}: Missing target register in load or store.\n'.format(self.current_line))
                    self.scanner.char_index = len(self.scanner.line)
                else:
                    tar_reg = int(self.word.lexeme[1:])
                    self.list.max_vr = max([self.list.max_vr, sour_reg, tar_reg])
                    ir = Op(op=lexeme, arg1=Argument(sr=sour_reg), arg3=Argument(sr=tar_reg))
                    node = Node(op=ir)
                    self.list.add(node)

    def finish_loadI(self):
        if self.scanner.line_error:
            self.scanner.line_error = False
            self.next_flag = True
            return
        lexeme = self.word.lexeme
        self.word = self.scanner.next_token()
        if (not self.word.opcode == 5 and self.current_line == self.word.line_num) or not self.current_line == self.word.line_num:
            self.error = True
            self.num_error += 1
            sys.stderr.write('{}: Missing constant in loadI.\n'.format(self.current_line))
            self.scanner.char_index = len(self.scanner.line)
        else:
            if self.scanner.line_error:
                self.scanner.line_error = False
                self.next_flag = True
                return
            const = int(self.word.lexeme)
            self.word = self.scanner.next_token()
            if (not self.word.opcode == 8 and self.current_line == self.word.line_num) or not self.current_line == self.word.line_num:
                self.error = True
                self.num_error += 1
                sys.stderr.write('{}: Missing "=>" in loadI.\n'.format(self.current_line))
                self.scanner.char_index = len(self.scanner.line)
            else:
                if self.scanner.line_error:
                    self.scanner.line_error = False
                    self.next_flag = True
                    return
                self.word = self.scanner.next_token()
                if (not self.word.opcode == 6 and self.current_line == self.word.line_num) or not self.current_line == self.word.line_num:
                    self.error = True
                    self.num_error += 1
                    sys.stderr.write('{}: Missing target register in loadI.\n'.format(self.current_line))
                    self.scanner.char_index = len(self.scanner.line)
                else:
                    tar_reg = int(self.word.lexeme[1:])
                    self.list.max_vr = max([self.list.max_vr, tar_reg])
                    ir = Op(op=lexeme, arg1=Argument(sr=const), arg3=Argument(sr=tar_reg))
                    node = Node(op=ir)
                    self.list.add(node)

    def finish_arithop(self):
        if self.scanner.line_error:
            self.scanner.line_error = False
            self.next_flag = True
            return
        lexeme = self.word.lexeme
        self.word = self.scanner.next_token()
        if (not self.word.opcode == 6 and self.current_line == self.word.line_num) or not self.current_line == self.word.line_num:
            self.error = True
            self.num_error += 1
            sys.stderr.write('{}: Missing first source register in add or sub or mult.\n'.format(self.current_line))
            self.scanner.char_index = len(self.scanner.line)
        else:
            if self.scanner.line_error:
                self.scanner.line_error = False
                self.next_flag = True
                return
            first_sour_reg = int(self.word.lexeme[1:])
            self.word = self.scanner.next_token()
            if (not self.word.opcode == 7 and self.current_line == self.word.line_num) or not self.current_line == self.word.line_num:
                self.error = True
                self.num_error += 1
                sys.stderr.write(
                    '{}: Missing comma in add or sub or mult.\n'.format(self.current_line))
                self.scanner.char_index = len(self.scanner.line)
            else:
                if self.scanner.line_error:
                    self.scanner.line_error = False
                    self.next_flag = True
                    return
                self.word = self.scanner.next_token()
                if (not self.word.opcode == 6 and self.current_line == self.word.line_num) or not self.current_line == self.word.line_num:
                    self.error = True
                    self.num_error += 1
                    sys.stderr.write('{}: Missing second source register in add or sub or mult.\n'.format(self.current_line))
                    self.scanner.char_index = len(self.scanner.line)
                else:
                    if self.scanner.line_error:
                        self.scanner.line_error = False
                        self.next_flag = True
                        return
                    second_sour_reg = int(self.word.lexeme[1:])
                    self.word = self.scanner.next_token()
                    if (not self.word.opcode == 8 and self.current_line == self.word.line_num) or not self.current_line == self.word.line_num:
                        self.error = True
                        self.num_error += 1
                        sys.stderr.write('{}: Missing "=>" in in add or sub or mult.\n'.format(self.current_line))
                        self.scanner.char_index = len(self.scanner.line)
                    else:
                        if self.scanner.line_error:
                            self.scanner.line_error = False
                            self.next_flag = True
                            return
                        self.word = self.scanner.next_token()
                        if (not self.word.opcode == 6 and self.current_line == self.word.line_num) or not self.current_line == self.word.line_num:
                            self.error = True
                            self.num_error += 1
                            sys.stderr.write('{}: Missing target register in add or sub or mult.\n'.format(self.current_line))
                            self.scanner.char_index = len(self.scanner.line)
                        else:
                            tar_reg = int(self.word.lexeme[1:])
                            self.list.max_vr = max([self.list.max_vr, first_sour_reg, second_sour_reg, tar_reg])
                            ir = Op(op=lexeme, arg1=Argument(sr=first_sour_reg), arg2=Argument(sr=second_sour_reg), arg3=Argument(sr=tar_reg))
                            node = Node(op=ir)
                            self.list.add(node)

    def finish_output(self):
        if self.scanner.line_error:
            self.scanner.line_error = False
            self.next_flag = True
            return
        lexeme = self.word.lexeme
        self.word = self.scanner.next_token()
        if (not self.word.opcode == 5 and self.current_line == self.word.line_num) or not self.current_line == self.word.line_num:
            self.error = True
            self.num_error += 1
            sys.stderr.write('{}: Missing constant in output.\n'.format(self.current_line))
            self.scanner.char_index = len(self.scanner.line)
        else:
            const = int(self.word.lexeme)
            ir = Op(op=lexeme, arg1=Argument(sr=const))
            node = Node(op=ir)
            self.list.add(node)

    def finish_nop(self):
        lexeme = self.word.lexeme
        ir = Op(op=lexeme)
        node = Node(op=ir)
        self.list.add(node)

