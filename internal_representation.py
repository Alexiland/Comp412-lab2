import os
import sys

class Node(object):
    def __init__(self, op):
        self.value = op
        self.prev = None
        self.next = None

    def __str__(self):
        return str(self.value)


class IR(object):
    def __init__(self):
        self.__head = None
        self.dummy_head = None
        self.dummy_tail = None
        self.max_vr = 0
        self.max_live = 0

    def is_empty(self):
        return self.__head is None

    def __len__(self):
        count = 0
        cur = self.dummy_head
        while cur:
            count += 1
            cur = cur.next
        return count

    def traverse(self):
        cur = self.dummy_head
        while cur:
            sys.stdout.write('{}'.format(cur.value))
            cur = cur.next

    def reverse_traverse(self):
        cur = self.dummy_tail
        while cur:
            sys.stdout.write('{}'.format(cur.value))
            cur = cur.prev

    def add(self, value):
        node = Node(value)
        if self.is_empty():
            self.__head = node
            self.dummy_head = node
            self.dummy_tail = node
        else:
            node.prev = self.__head
            self.__head.next = node
            self.dummy_tail = node
            self.__head = node

    def add_prev(self, value):
        node = Node(value)
        if self.is_empty():
            self.__head = node
            self.dummy_head = node
            self.dummy_tail = node
        else:
            prev = self.__head.prev
            prev.next = node
            node.prev = prev
            node.next = self.__head
            self.__head.prev = node



    def append(self, value):
        node = Node(value)
        cur = self.__head
        if self.is_empty():
            self.__head = Node
            return
        while cur.next:
            cur = cur.next
        cur.next = node
        node.prev = cur
        self.dummy_tail = node

    def insert(self, pos, value):
        if pos <= 0:
            self.add(value)
        elif pos > len(self) - 1:
            self.append(value)
        else:
            node = Node(value)
            count = 0
            cur = self.__head
            while count < pos - 1:
                count += 1
                cur = cur.next
            node.next = cur.next
            cur.next.prev = node
            node.prev = cur
            cur.next = node

    def search(self, value):
        cur = self.__head
        while cur:
            if cur.value == value:
                return True
            else:
                cur = cur.next
        return False

    def remove(self, value):
        if self.is_empty():
            return
        cur = self.__head
        while cur:
            if cur.value == value:
                if cur == self.__head:
                    self.__head = cur.next
                    if cur.next:
                        cur.next.prev = None
                else:
                    cur.prev.next = cur.next
                    if cur.next:
                        cur.next.prev = cur.prev
                return
            else:
                cur = cur.next

class Op(object):
    def __init__(self, op, arg1=None, arg2=None, arg3=None):
        self.op = op
        self.operand1 = arg1
        self.operand2 = arg2
        self.operand3 = arg3

    # def __str__(self):
    #     if self.op == 'load':
    #         return 'load    [ {} ], [ ], [ {} ]\n'.format(self.operand1.sr, self.operand3.sr)
    #     elif self.op == 'store':
    #         return 'store   [ {} ], [ ], [ {} ]\n'.format(self.operand1.sr, self.operand3.sr)
    #     elif self.op == 'loadI':
    #         return 'loadI   [ {} ], [ ], [ {} ]\n'.format(self.operand1.sr, self.operand3.sr)
    #     elif self.op == 'add':
    #         return 'add     [ {} ], [ {} ], [ {} ]\n'.format(self.operand1.sr, self.operand2.sr, self.operand3.sr)
    #     elif self.op == 'sub':
    #         return 'sub     [ {} ], [ {} ], [ {} ]\n'.format(self.operand1.sr, self.operand2.sr, self.operand3.sr)
    #     elif self.op == 'mult':
    #         return 'mult	[ {} ], [ {} ], [ {} ]\n'.format(self.operand1.sr, self.operand2.sr, self.operand3.sr)
    #     elif self.op == 'lshift':
    #         return 'lshift  [ {} ], [ {} ], [ {} ]\n'.format(self.operand1.sr, self.operand2.sr, self.operand3.sr)
    #     elif self.op == 'rshift':
    #         return 'rshift  [ {} ], [ {} ], [ {} ]\n'.format(self.operand1.sr, self.operand2.sr, self.operand3.sr)
    #     elif self.op == 'output':
    #         return 'output  [ {} ], [ ], [ ]\n'.format(self.operand1.sr)
    #     elif self.op == 'nop':
    #         return 'nop [ ], [ ], [ ]\n'

    # def __str__(self):
    #     if self.op == 'load':
    #         return 'load    {} => {}\n'.format(self.operand1, self.operand3)
    #     elif self.op == 'store':
    #         return 'store   {} => {}\n'.format(self.operand1, self.operand3)
    #     elif self.op == 'loadI':
    #         return 'loadI   {} => {}\n'.format(self.operand1.sr, self.operand3)
    #     elif self.op == 'add':
    #         return 'add     {}, {} => {}\n'.format(self.operand1, self.operand2, self.operand3)
    #     elif self.op == 'sub':
    #         return 'sub     {}, {} => {}\n'.format(self.operand1, self.operand2, self.operand3)
    #     elif self.op == 'mult':
    #         return 'mult	{}, {} => {}\n'.format(self.operand1, self.operand2, self.operand3)
    #     elif self.op == 'lshift':
    #         return 'lshift  {}, {} => {}\n'.format(self.operand1, self.operand2, self.operand3)
    #     elif self.op == 'rshift':
    #         return 'rshift  {}, {} => {}\n'.format(self.operand1, self.operand2, self.operand3)
    #     elif self.op == 'output':
    #         return 'output  {}\n'.format(self.operand1.sr)
    #     elif self.op == 'nop':
    #         return 'nop \n'

    def __str__(self):
        if self.op == 'load':
            return 'load    {} => {}\n'.format("r"+str(self.operand1.pr), "r"+str(self.operand3.pr))
        elif self.op == 'store':
            return 'store   {} => {}\n'.format("r"+str(self.operand1.pr), "r"+str(self.operand3.pr))
        elif self.op == 'loadI':
            return 'loadI   {} => {}\n'.format(self.operand1.sr, "r"+str(self.operand3.pr))
        elif self.op == 'add':
            return 'add     {}, {} => {}\n'.format("r"+str(self.operand1.pr), "r"+str(self.operand2.pr), "r"+str(self.operand3.pr))
        elif self.op == 'sub':
            return 'sub     {}, {} => {}\n'.format("r"+str(self.operand1.pr), "r"+str(self.operand2.pr), "r"+str(self.operand3.pr))
        elif self.op == 'mult':
            return 'mult	{}, {} => {}\n'.format("r"+str(self.operand1.pr), "r"+str(self.operand2.pr), "r"+str(self.operand3.pr))
        elif self.op == 'lshift':
            return 'lshift  {}, {} => {}\n'.format("r"+str(self.operand1.pr), "r"+str(self.operand2.pr), "r"+str(self.operand3.pr))
        elif self.op == 'rshift':
            return 'rshift  {}, {} => {}\n'.format("r"+str(self.operand1.pr), "r"+str(self.operand2.pr), "r"+str(self.operand3.pr))
        elif self.op == 'output':
            return 'output  {}\n'.format(self.operand1.sr)
        elif self.op == 'nop':
            return 'nop \n'



class Argument(object):
    def __init__(self, sr=None, vr=None, pr=None, nu=None):
        self.sr = sr
        self.vr = vr
        self.pr = pr
        self.nu = nu

    def __str__(self):
        return "[{}, {}, {}, {}]".format("sr" + str(self.sr) if self.sr is not None else self.sr,
                                         "vr" + str(self.vr) if self.vr is not None else self.vr,
                                         "pr" + str(self.pr) if self.pr is not None else self.pr,
                                         self.nu)

class PR(object):
    def __init__(self, addr):
        self.addr = addr
        self.in_use = False

    def __str__(self):
        return 'pr'+str(self.addr)

    def set_mark(self):
        self.in_use = True

    def clear_mark(self):
        self.in_use = False