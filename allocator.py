from parser import *
from rename_register import *
from Queue import *
from internal_representation import *

ADDRESS = 0
CONSTANT = 1

class Allocator(object):
    def __init__(self, ir, k):
        """
        :param ir: internal representation from parser and after renaming process
        :param k: number of true physical register. from 3 to 64
        """
        self.ir = ir
        self.k = k

        self.queue = Queue()
        if self.k < self.ir.max_live:
            self.no_spill = False
            self.vr_to_pr = [None] * (self.ir.max_vr + 1)
            self.pr_to_vr = [None] * (self.k - 1)
            self.spill_reg = self.k - 1
            for i in range(self.k - 1):
                self.queue.put(i)
        else:
            self.no_spill = True
            self.spill_reg = None
            self.vr_to_pr = [None] * (self.ir.max_vr + 1)
            self.pr_to_vr = [None] * (self.k)
            for i in range(self.k):
                self.queue.put(i)
        self.pr_nu = self.pr_to_vr[:]
        self.vr_to_spill_loc = self.vr_to_pr[:]
        self.reserved_reg_flag = False

        self.new_ir = IR()
        self.mem_loc = 32768
        self.reserved_pr = None


    def allocate_registers(self):
        vr_to_pr = self.vr_to_pr
        queue = self.queue

        op = self.ir.dummy_head
        while op is not None:
            # clear the mark in each PR
            self.reserved_pr = None

            if op.value.value.op == 'add' \
                    or op.value.value.op == 'sub' or op.value.value.op == 'mult' or \
                    op.value.value.op == 'lshift' or op.value.value.op == 'rshift':
                vr1 = op.value.value.operand1.vr
                vr2 = op.value.value.operand2.vr
                vr3 = op.value.value.operand3.vr
                if vr1 is not None:
                    pr = vr_to_pr[op.value.value.operand1.vr]
                    if pr is None:
                        op.value.value.operand1.pr = self.get_a_pr(op.value.value.operand1.vr, op.value.value.operand1.nu, op)
                        self.restore(op.value.value.operand1.vr, op.value.value.operand1.pr, op.value.value.operand1.nu)
                    else:
                        op.value.value.operand1.pr = pr
                    # set the mark in U.PR
                    self.reserved_pr = op.value.value.operand1.pr

                if vr2 is not None:
                    pr = vr_to_pr[op.value.value.operand2.vr]
                    if pr is None:
                        op.value.value.operand2.pr = self.get_a_pr(op.value.value.operand2.vr, op.value.value.operand2.nu, op)
                        self.restore(op.value.value.operand2.vr, op.value.value.operand2.pr, op.value.value.operand2.nu)
                    else:
                        op.value.value.operand2.pr = pr
                    # set the mark in U.PR
                    self.reserved_pr = op.value.value.operand2.pr

                if vr1 is not None:
                    if op.value.value.operand1.nu is None and op.value.value.operand1.pr is not None:
                        self.free_a_pr(op.value.value.operand1.pr, op, op.value.value.operand1.vr)
                        queue.put(op.value.value.operand1.pr)

                if vr2 is not None:
                    if op.value.value.operand2.nu is None and op.value.value.operand2.pr is not None:
                        self.free_a_pr(op.value.value.operand2.pr, op, op.value.value.operand2.vr)
                        queue.put(op.value.value.operand2.pr)

                self.reserved_pr = None
                self.reserved_reg_flag = False

                if vr3 is not None and op.value.value.operand3.nu is not None:
                    op.value.value.operand3.pr = self.get_a_pr(op.value.value.operand3.vr, op.value.value.operand3.nu, op)
                    self.new_ir.add(op)

                if op.value.value.operand3.nu is None and op.value.value.operand3.pr is not None:
                    self.free_a_pr(op.value.value.operand3.pr, op, op.value.value.operand3.vr)
                    queue.put(op.value.value.operand3.pr)


            elif op.value.value.op == 'load':
                vr1 = op.value.value.operand1.vr
                vr3 = op.value.value.operand3.vr

                if vr1 is not None:
                    pr = vr_to_pr[op.value.value.operand1.vr]
                    if pr is None:
                        op.value.value.operand1.pr = self.get_a_pr(op.value.value.operand1.vr, op.value.value.operand1.nu, op)
                        self.restore(op.value.value.operand1.vr, op.value.value.operand1.pr, op.value.value.operand1.nu)
                    else:
                        op.value.value.operand1.pr = pr
                    # set the mark in U.PR
                    self.reserved_pr = op.value.value.operand1.pr

                if vr1 is not None:
                    if op.value.value.operand1.nu is None and op.value.value.operand1.pr is not None:
                        self.free_a_pr(op.value.value.operand1.pr, op, op.value.value.operand1.vr)
                        queue.put(op.value.value.operand1.pr)

                # clear the mark in each PR
                self.reserved_pr = None
                self.reserved_reg_flag = False

                if vr3 is not None and op.value.value.operand3.nu is not None:
                    op.value.value.operand3.pr = self.get_a_pr(op.value.value.operand3.vr, op.value.value.operand3.nu, op)
                    self.new_ir.add(op)

                if op.value.value.operand3.nu is None and op.value.value.operand3.pr is not None:
                    self.free_a_pr(op.value.value.operand3.pr, op, op.value.value.operand3.vr)
                    queue.put(op.value.value.operand3.pr)


            elif op.value.value.op == 'store':
                vr1 = op.value.value.operand1.vr
                vr3 = op.value.value.operand3.vr

                if vr1 is not None:
                    pr = vr_to_pr[op.value.value.operand1.vr]
                    if pr is None:
                        op.value.value.operand1.pr = self.get_a_pr(op.value.value.operand1.vr,
                                                                   op.value.value.operand1.nu, op)
                        self.restore(op.value.value.operand1.vr, op.value.value.operand1.pr, op.value.value.operand1.nu)
                    else:
                        op.value.value.operand1.pr = pr
                    # set the mark in U.PR
                    self.reserved_pr = op.value.value.operand1.pr

                if vr3 is not None:
                    pr = vr_to_pr[op.value.value.operand3.vr]
                    if pr is None:
                        op.value.value.operand3.pr = self.get_a_pr(op.value.value.operand3.vr,
                                                                   op.value.value.operand3.nu, op)
                        self.restore(op.value.value.operand3.vr, op.value.value.operand3.pr, op.value.value.operand3.nu)
                    else:
                        op.value.value.operand3.pr = pr
                    # set the mark in U.PR
                    self.reserved_pr = op.value.value.operand3.pr

                if vr1 is not None:
                    if op.value.value.operand1.nu is None and op.value.value.operand1.pr is not None:
                        self.free_a_pr(op.value.value.operand1.pr, op, op.value.value.operand1.vr)
                        queue.put(op.value.value.operand1.pr)

                if vr3 is not None:
                    if op.value.value.operand3.nu is None and op.value.value.operand3.pr is not None:
                        self.free_a_pr(op.value.value.operand3.pr, op, op.value.value.operand3.vr)
                        queue.put(op.value.value.operand3.pr)

                self.reserved_reg_flag = False
                self.new_ir.add(op)

            elif op.value.value.op == 'loadI':
                vr3 = op.value.value.operand3.vr

                if vr3 is not None and op.value.value.operand3.nu is not None:
                    if self.spill_reg is not None:
                        self.vr_to_spill_loc[vr3] = (CONSTANT, op.value.value.operand1.sr)
                    else:
                        op.value.value.operand3.pr = self.get_a_pr(op.value.value.operand3.vr,
                                                                   op.value.value.operand3.nu, op)
                        self.new_ir.add(op)
                # clear the mark in each PR
                self.reserved_pr = None
            else:
                self.new_ir.add(op)

            op = op.next
        return self.new_ir


    def get_a_pr(self, vr, nu, op):
        if not self.queue.empty():
            x = self.queue.get()
            self.vr_to_pr[vr] = x
            self.pr_to_vr[x] = vr
            self.pr_nu[x] = nu
            return x
        else:
            # default heuristic: max_nu
            max_nu_1 = 0
            max_index_1 = 0
            for index, nu in enumerate(self.pr_nu):
                if index != self.reserved_pr and max_nu_1 <= nu:
                    max_nu_1 = nu
                    max_index_1 = index
            x_1 = max_index_1

            # heuristic 1: max_nu of clean value
            max_nu_2 = 0
            max_index_2 = 0
            for index, nu in enumerate(self.pr_nu):
                if index != self.reserved_pr and max_nu_2 <= nu and self.vr_to_spill_loc[vr] is not None:
                    max_nu_2 = nu
                    max_index_2 = index
            x_2 = max_index_2

            x = x_2
            self.spill(x)
            self.vr_to_pr[vr] = x
            self.pr_to_vr[x] = vr
            self.pr_nu[x] = nu
            return x

    def restore(self, vr, pr, nu):
        if self.vr_to_spill_loc[vr] is not None:
            _type, m = self.vr_to_spill_loc[vr]
            if _type == ADDRESS:
                self.new_ir.add(Node(op=Op(op="loadI", arg1=Argument(sr=m, vr=vr, pr=m),
                                                arg3=Argument(sr=self.spill_reg, vr=self.ir.max_vr + 1, pr=self.spill_reg))))
                self.new_ir.add(Node(op=Op(op="load", arg1=Argument(sr=self.ir.max_vr + 1, vr=vr, pr=self.spill_reg),
                                                arg3=Argument(sr=self.ir.max_vr + 1, vr=self.ir.max_vr + 1,
                                                              pr=pr))))
            elif _type == CONSTANT:
                self.new_ir.add(Node(op=Op(op="loadI", arg1=Argument(sr=m, vr=vr, pr=self.spill_reg),
                                           arg3=Argument(sr=self.ir.max_vr + 1, vr=self.ir.max_vr + 1,
                                                         pr=pr))))
            # self.vr_to_spill_loc[vr] = None
            self.vr_to_pr[vr] = pr
            self.pr_to_vr[pr] = vr
            self.pr_nu[pr] = nu


    def free_a_pr(self, pr, op, vr):
        self.vr_to_pr[self.pr_to_vr[pr]] = None
        self.pr_to_vr[pr] = None
        self.pr_nu[pr] = None

    def spill(self, x):
        vr = self.pr_to_vr[x]
        if self.vr_to_spill_loc[vr] is None:
            m = self.mem_loc
            self.mem_loc += 4
            self.vr_to_spill_loc[vr] = (ADDRESS, m)
            self.new_ir.add(Node(op=Op(op="loadI", arg1=Argument(sr=m, vr=vr, pr=m),
                                            arg3=Argument(sr=self.ir.max_vr + 1, vr=self.ir.max_vr + 1,
                                                          pr=self.spill_reg))))
            self.new_ir.add(Node(op=Op(op="store", arg1=Argument(sr=self.ir.max_vr + 1, vr=vr, pr=x),
                                            arg3=Argument(sr=self.ir.max_vr + 1, vr=self.ir.max_vr + 1,
                                                          pr=self.spill_reg))))

        self.vr_to_pr[vr] = None