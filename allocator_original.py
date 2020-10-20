from parser import *
from rename_register import *
from Queue import *
from internal_representation import *

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
            self.vr_to_pr = [None] * (self.ir.max_vr + 1)
            self.pr_to_vr = [None] * (self.k - 1)
            self.spill_reg = self.k - 1
            for i in range(self.k - 1):
                self.queue.put(i)
        else:
            self.vr_to_pr = [None] * (self.ir.max_vr + 1)
            self.pr_to_vr = [None] * (self.k)
            for i in range(self.k):
                self.queue.put(i)
        self.pr_nu = self.pr_to_vr[:]
        self.vr_to_spill_loc = self.vr_to_pr[:]

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
                        self.free_a_pr(op.value.value.operand1.pr, op)
                        queue.put(op.value.value.operand1.pr)

                if vr2 is not None:
                    if op.value.value.operand2.nu is None and op.value.value.operand2.pr is not None:
                        self.free_a_pr(op.value.value.operand2.pr, op)
                        queue.put(op.value.value.operand2.pr)

                self.reserved_pr = None

                if vr3 is not None and op.value.value.operand3.nu is not None:
                    op.value.value.operand3.pr = self.get_a_pr(op.value.value.operand3.vr, op.value.value.operand3.nu, op)


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
                        self.free_a_pr(op.value.value.operand1.pr, op)
                        queue.put(op.value.value.operand1.pr)

                # clear the mark in each PR
                self.reserved_pr = None

                if vr3 is not None:
                    op.value.value.operand3.pr = self.get_a_pr(op.value.value.operand3.vr, op.value.value.operand3.nu, op)

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
                        self.free_a_pr(op.value.value.operand1.pr, op)
                        queue.put(op.value.value.operand1.pr)

                if vr3 is not None:
                    if op.value.value.operand3.nu is None and op.value.value.operand3.pr is not None:
                        self.free_a_pr(op.value.value.operand3.pr, op)
                        queue.put(op.value.value.operand3.pr)

            elif op.value.value.op == 'loadI':
                vr3 = op.value.value.operand3.vr

                if vr3 is not None and op.value.value.operand3.nu is not None:
                    op.value.value.operand3.pr = self.get_a_pr(op.value.value.operand3.vr, op.value.value.operand3.nu, op)

                # clear the mark in each PR
                self.reserved_pr = None

            # print("after pr assignment op:{}".format(op))
            self.new_ir.add(op)
            op = op.next

        return self.new_ir


    def get_a_pr(self, vr, nu, op):
        if not self.queue.empty():
            x = self.queue.get()
        else:
            max_nu = 0
            max_index = 0
            for index, nu in enumerate(self.pr_nu):
                if index != self.reserved_pr and max_nu <= nu:
                    max_nu = nu
                    max_index = index
            x = max_index
            self.spill(x)
        self.vr_to_pr[vr] = x
        self.pr_to_vr[x] = vr
        self.pr_nu[x] = nu
        return x

    def restore(self, vr, pr, nu):
        m = self.vr_to_spill_loc[vr]
        self.new_ir.add(Node(op=Op(op="loadI", arg1=Argument(sr=m, vr=vr, pr=m),
                                        arg3=Argument(sr=self.spill_reg, vr=self.ir.max_vr + 1, pr=self.spill_reg))))
        self.new_ir.add(Node(op=Op(op="load", arg1=Argument(sr=self.ir.max_vr + 1, vr=vr, pr=self.spill_reg),
                                        arg3=Argument(sr=self.ir.max_vr + 1, vr=self.ir.max_vr + 1,
                                                      pr=pr))))
        self.vr_to_spill_loc[vr] = None
        self.vr_to_pr[vr] = pr
        self.pr_to_vr[pr] = vr
        self.pr_nu[pr] = nu


    def free_a_pr(self, pr, op):
        self.vr_to_pr[self.pr_to_vr[pr]] = None
        self.pr_to_vr[pr] = None
        self.pr_nu[pr] = None

    def spill(self, x):
        m = self.mem_loc
        self.mem_loc += 4
        vr = self.pr_to_vr[x]
        self.vr_to_spill_loc[vr] = m
        self.new_ir.add(Node(op=Op(op="loadI", arg1=Argument(sr=m, vr=vr, pr=m),
                                        arg3=Argument(sr=self.ir.max_vr + 1, vr=self.ir.max_vr + 1,
                                                      pr=self.spill_reg))))
        self.new_ir.add(Node(op=Op(op="store", arg1=Argument(sr=self.ir.max_vr + 1, vr=vr, pr=x),
                                        arg3=Argument(sr=self.ir.max_vr + 1, vr=self.ir.max_vr + 1,
                                                      pr=self.spill_reg))))

        self.vr_to_pr[vr] = None