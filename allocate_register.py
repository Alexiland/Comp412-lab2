from parser import *
from rename_register import *

CONSTANT = 0
ADDRESS = 1

class Allocator(object):
    def __init__(self, ir, k):
        self.ir = ir
        self.k = k

        self.spill_reg = self.k - 1
        self.pr_to_vr = [None] * (self.k - 1)
        self.vr_to_pr = [None] * (self.ir.max_vr + 1)
        self.vr_spill = self.vr_to_pr[:]
        self.vr_nu = self.vr_spill[:]
        self.pr_nu = self.pr_to_vr[:]

        self.new_ir = IR()

        # Location for spilling memory
        self.mem_loc = 32772
        self.open_addr = []

        self.reserved_vr = None

    def allocate_registers(self):
        vr_to_pr = self.vr_to_pr
        vr_nu = self.vr_nu

        op = self.ir.dummy_head

        while op is not None:
            vr1 = op.value.value.operand1.vr
            vr2 = op.value.value.operand2.vr
            vr3 = op.value.value.operand3.vr

            # Store LOADI values for rematerialization later.
            if op.value.value.op == 'loadI':
                self.vr_spill[vr3] = (CONSTANT, op.value.value.operand1.sr)
                vr_nu[vr3] = op.value.value.operand3.nu
                op = op.next
                continue

            # Unused declaration.
            if vr3 is not None and op.value.value.operand3.nu is None:
                if vr1 is not None:
                    if op.value.value.operand2.nu is not None:
                        vr_nu[vr1] = op.value.value.operand1.nu
                    else:
                        self.clear_vr(vr1)
                if vr2 is not None:
                    if op.value.value.operand2.nu is not None:
                        vr_nu[vr2] = op.value.value.operand3.nu
                    else:
                        self.clear_vr(vr2)
                op = op.next
                continue

            if vr1 is not None:
                if vr_to_pr[vr1] is not None:
                    op.value.value.operand1.pr = vr_to_pr[vr1]
                else:
                    # Retrieve spilled value
                    self.reserved_vr = vr2
                    p = self.unspill(vr1)
                    op.value.value.operand1.pr = p

            if vr2 is not None:
                if vr_to_pr[vr2] is not None:
                    op.value.value.operand2.pr = vr_to_pr[vr2]
                else:
                    # Retrieve spilled value
                    self.reserved_vr = vr1
                    p = self.unspill(vr2)
                    op.value.value.operand2.pr = p

            self.reserved_vr = None

            # Update next use and clear regs if necessary. Clearing before
            # handling r3 allows for reuse of the same registers within an expression.
            if vr1 is not None:
                if op.value.value.operand1.nu is not None:
                    vr_nu[vr1] = op.value.value.operand1.nu
                else:
                    self.clear_vr(vr1)
            if vr2 is not None:
                if op.value.value.operand2.nu is not None:
                    vr_nu[vr2] = op.value.value.operand2.nu
                else:
                    self.clear_vr(vr2)

            # vr3 corresponds to new declaration, so always needs new pr
            if vr3 is not None:
                p = self.get_pr()
                self.assign_pr(vr3, p)

                op.value.value.operand3.pr = p

            # Update next use of vr3
            if vr3 is not None:
                if op.value.value.operand3.nu is not None:
                    vr_nu[vr3] = op.value.value.operand3.nu
                else:
                    self.clear_vr(vr3)

            self.new_ir.add(op)
            op = op.next


    def clear_vr(self, vr):

        p = self.vr_to_pr[vr]

        if p is not None:
            self.pr_to_vr[p] = None
            self.vr_to_pr[vr] = None
            if self.vr_spill[vr]:
                if self.vr_spill[vr][0] == ADDRESS:
                    self.open_addr.append(self.vr_spill[vr][1])
                self.vr_spill[vr] = None

    def get_pr(self):
        """
        """

        try:
            return self.pr_to_vr.index(None)

        except ValueError:
            return self.spill()

    def spill(self):
        """
        """

        # If some value is already stored somewhere, you don't need to store it again.
        # This includes all values declared with a loadI.
        clean_vrs = [
            vr for vr in self.pr_to_vr
            if self.vr_spill[vr] is not None and vr != self.reserved_vr
        ]
        if clean_vrs:
            vr = max(clean_vrs, key=lambda v: self.vr_nu[v])
            pr = self.vr_to_pr[vr]
            self.vr_to_pr[vr] = None
            self.pr_to_vr[pr] = None
            return pr

        pr = self.pr_to_vr.index(
            max(self.pr_to_vr, key=lambda v: self.vr_nu[v] * int(v != self.reserved_vr))
        )

        if not self.open_addr:
            m = self.mem_loc
            self.mem_loc += 4

        else:
            m = self.open_addr.pop()

        vr = self.pr_to_vr[pr]

        self.new_ir.add(Node(op=Op(op="loadI", arg1=Argument(sr=-2, vr=vr, pr=m), arg3=Argument(sr=self.ir.max_vr + 1, vr=self.ir.max_vr + 1, pr=self.spill_reg))))
        self.new_ir.add(Node(op=Op(op="store", arg1=Argument(sr=self.ir.max_vr + 1, vr=vr, pr=pr), arg3=Argument(sr=self.ir.max_vr + 1, vr=self.ir.max_vr + 1, pr=self.spill_reg))))

        self.vr_to_pr[vr] = None
        self.pr_to_vr[pr] = None
        self.vr_spill[vr] = (ADDRESS, m)

        return pr

    def unspill(self, vr):
        """
        """
        pr = self.get_pr()

        spill_val = self.vr_spill[vr]

        # Get address of spilled value
        if spill_val is not None:

            if spill_val[0] == ADDRESS:

                self.new_ir.add(Node(op=Op(op="loadI", arg1=Argument(sr=-1, vr=vr, pr=spill_val[1]),
                                           arg3=Argument(sr=self.spill_reg, vr=self.ir.max_vr + 1,
                                                         pr=self.spill_reg))))

                self.new_ir.add(Node(op=Op(op="load", arg1=Argument(sr=self.ir.max_vr + 1, vr=vr, pr=self.spill_reg),
                                           arg3=Argument(sr=self.ir.max_vr + 1, vr=self.ir.max_vr + 1,
                                                         pr=pr))))

            elif spill_val[0] == CONSTANT:
                self.new_ir.add(Node(op=Op(op="loadI", arg1=Argument(sr=-3, vr=vr, pr=spill_val[1]),
                                           arg3=Argument(sr=self.ir.max_vr + 1, vr=self.ir.max_vr + 1,
                                                         pr=pr))))
        else:
            self.new_ir.add(Node(op=Op(op="loadI", arg1=Argument(sr=-3, vr=vr, pr=0),
                                       arg3=Argument(sr=self.ir.max_vr + 1, vr=self.ir.max_vr + 1,
                                                     pr=pr))))

        self.assign_pr(vr, pr)

        return pr

    def assign_pr(self, vr, pr):

        self.vr_to_pr[vr] = pr
        self.pr_to_vr[pr] = vr