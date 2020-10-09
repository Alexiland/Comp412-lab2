from parser import *
from scanner import *
from internal_representation import *

def rename_register(IR):
    vr_name = 0
    sr_to_vr = [None] * (IR.max_vr + 1)
    lu = sr_to_vr[:]

    Op = IR.dummy_tail
    index = len(IR)

    while Op is not None:
        if Op.value.value.op == 'load' or Op.value.value.op == 'add' \
                or Op.value.value.op == 'sub' or Op.value.value.op == 'mult' or \
                Op.value.value.op == 'lshift' or Op.value.value.op == 'rshift':

            # Check register def
            if Op.value.value.operand3 is not None:
                if sr_to_vr[Op.value.value.operand3.sr] is None:
                    sr_to_vr[Op.value.value.operand3.sr] = vr_name
                    vr_name += 1

                Op.value.value.operand3.vr = sr_to_vr[Op.value.value.operand3.sr]
                Op.value.value.operand3.nu = lu[Op.value.value.operand3.sr]
                sr_to_vr[Op.value.value.operand3.sr] = None
                lu[Op.value.value.operand3.sr] = None

            if Op.value.value.operand1 is not None:
                if sr_to_vr[Op.value.value.operand1.sr] is None:
                    sr_to_vr[Op.value.value.operand1.sr] = vr_name
                    vr_name += 1

                Op.value.value.operand1.vr = sr_to_vr[Op.value.value.operand1.sr]
                Op.value.value.operand1.nu = lu[Op.value.value.operand1.sr]
                lu[Op.value.value.operand1.sr] = index

            if Op.value.value.operand2 is not None:
                if sr_to_vr[Op.value.value.operand2.sr] is None:
                    sr_to_vr[Op.value.value.operand2.sr] = vr_name
                    vr_name += 1

                Op.value.value.operand2.vr = sr_to_vr[Op.value.value.operand2.sr]
                Op.value.value.operand2.nu = lu[Op.value.value.operand2.sr]
                lu[Op.value.value.operand2.sr] = index

            index = index - 1
        elif Op.value.value.op == 'store':

            if Op.value.value.operand3 is not None:
                if sr_to_vr[Op.value.value.operand3.sr] is None:
                    sr_to_vr[Op.value.value.operand3.sr] = vr_name
                    vr_name += 1

                Op.value.value.operand3.vr = sr_to_vr[Op.value.value.operand3.sr]
                Op.value.value.operand3.nu = lu[Op.value.value.operand3.sr]
                lu[Op.value.value.operand3.sr] = index
            if Op.value.value.operand1 is not None:
                if sr_to_vr[Op.value.value.operand1.sr] is None:
                    sr_to_vr[Op.value.value.operand1.sr] = vr_name
                    vr_name += 1

                Op.value.value.operand1.vr = sr_to_vr[Op.value.value.operand1.sr]
                Op.value.value.operand1.nu = lu[Op.value.value.operand1.sr]
                lu[Op.value.value.operand1.sr] = index

            index = index - 1
        elif Op.value.value.op == "loadI":
            if Op.value.value.operand3 is not None:
                if sr_to_vr[Op.value.value.operand3.sr] is None:
                    sr_to_vr[Op.value.value.operand3.sr] = vr_name
                    vr_name += 1

                Op.value.value.operand3.vr = sr_to_vr[Op.value.value.operand3.sr]
                Op.value.value.operand3.nu = lu[Op.value.value.operand3.sr]
                sr_to_vr[Op.value.value.operand3.sr] = None
                lu[Op.value.value.operand3.sr] = None
            index = index - 1
        Op = Op.prev

