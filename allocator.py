from parser import *
from rename_register import *
from queue import *


class Allocator(object):
    def __init__(self, ir, k):
        """
        :param ir: internal representation from parser and after renaming process
        :param k: number of true physical register. from 3 to 64
        """
        self.ir = ir
        self.k = k

        self.vr_to_pr = [None] * (self.ir.max_vr + 1)
        self.pr_to_vr = [None] * (self.k + 1)
        self.pr_nu = self.pr_to_vr[:]
        self.queue = Queue()
        for i in range(self.k+1):
            self.queue.put(i)

    def allocate(self):
        vr_to_pr = self.vr_to_pr
        pr_to_vr = self.pr_to_vr
        pr_nu = self.pr_nu
        queue = self.queue

        op = self.ir.dummy_head

        while op is not None:
            vr1 = op.value.value.operand1.vr
            vr2 = op.value.value.operand2.vr
            vr3 = op.value.value.operand3.vr

            if op.value.value.op == 'load' or op.value.value.op == 'add' \
                    or op.value.value.op == 'sub' or op.value.value.op == 'mult' or \
                    op.value.value.op == 'lshift' or op.value.value.op == 'rshift':
                #TODO: clear the mark in each PR

                if vr1 is not None:
                    pr = vr_to_pr[op.value.value.operand1.vr]
                    if pr is None:
                        op.value.value.operand1.pr = self.get_a_pr(op.value.value.operand1.vr, op.value.value.operand1.nu)
                        self.restore(op.value.value.operand1.vr, op.value.value.operand1.nu)
                    else:
                        op.value.value.operand1.pr = pr
                    op.value.value.operand1.pr.set_mark()

                if vr2 is not None:
                    pr = vr_to_pr[op.value.value.operand2.vr]
                    if pr is None:
                        op.value.value.operand2.pr = self.get_a_pr(op.value.value.operand2.vr, op.value.value.operand2.nu)
                        self.restore(op.value.value.operand2.vr, op.value.value.operand2.nu)
                    else:
                        op.value.value.operand2.pr = pr
                    # TODO: set the mark in U.PR

                if vr1 is not None:
                    if op.value.value.operand1.nu is None and op.value.value.operand1.pr is not None:
                        self.free_a_pr(op.value.value.operand1.pr)
                        queue.put(op.value.value.operand1.pr)

                if vr2 is not None:
                    if op.value.value.operand2.nu is None and op.value.value.operand2.pr is not None:
                        self.free_a_pr(op.value.value.operand2.pr)
                        queue.put(op.value.value.operand2.pr)

                # TODO: clear the mark in each PR

                if vr3 is not None:
                    op.value.value.operand3.pr = self.get_a_pr(op.value.value.operand3.vr, op.value.value.operand3.nu)
                    # TODO: set the mark in U.PR

    def get_a_pr(self, vr, nu):
        if self.queue.not_empty:
            x = self.queue.get()
        else:
            x = None
            # TODO: pick an unmarked x to spill
            self.spill(x)
        self.vr_to_pr[vr] = x
        self.pr_to_vr[x] = vr
        self.pr_nu[x] = nu
        return x

    def restore(self, vr, pr):
        pass

    def free_a_pr(self, pr):
        self.vr_to_pr[self.pr_to_vr[pr]] = None
        self.pr_to_vr[pr] = None
        self.pr_nu = None

    def spill(self, x):
        pass