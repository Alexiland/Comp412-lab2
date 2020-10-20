from parser import *
from scanner import *
from internal_representation import *

def rename_register(IR):
    vr_name = 0
    sr_to_vr = [None] * (IR.max_vr + 1)
    lu = sr_to_vr[:]

    Op = IR.dummy_tail
    index = len(IR)

    max_live = 0
    cur_live = 0

    while Op is not None:
        if Op.value.value.op == 'add' \
                or Op.value.value.op == 'sub' or Op.value.value.op == 'mult' or \
                Op.value.value.op == 'lshift' or Op.value.value.op == 'rshift':
            # Check register def
            if sr_to_vr[Op.value.value.operand3.sr] is None:
                sr_to_vr[Op.value.value.operand3.sr] = vr_name
                vr_name += 1
            else:
                cur_live = cur_live - 1
            Op.value.value.operand3.vr = sr_to_vr[Op.value.value.operand3.sr]
            Op.value.value.operand3.nu = lu[Op.value.value.operand3.sr]
            sr_to_vr[Op.value.value.operand3.sr] = None
            lu[Op.value.value.operand3.sr] = None


            if sr_to_vr[Op.value.value.operand1.sr] is None:
                sr_to_vr[Op.value.value.operand1.sr] = vr_name
                vr_name += 1
                cur_live = cur_live + 1
            Op.value.value.operand1.vr = sr_to_vr[Op.value.value.operand1.sr]
            Op.value.value.operand1.nu = lu[Op.value.value.operand1.sr]
            lu[Op.value.value.operand1.sr] = index

            if sr_to_vr[Op.value.value.operand2.sr] is None:
                sr_to_vr[Op.value.value.operand2.sr] = vr_name
                vr_name += 1
                cur_live = cur_live + 1
            Op.value.value.operand2.vr = sr_to_vr[Op.value.value.operand2.sr]
            Op.value.value.operand2.nu = lu[Op.value.value.operand2.sr]
            lu[Op.value.value.operand2.sr] = index

        elif Op.value.value.op == 'load':
            # Check register def
            if sr_to_vr[Op.value.value.operand3.sr] is None:
                sr_to_vr[Op.value.value.operand3.sr] = vr_name
                vr_name += 1
            else:
                cur_live = cur_live - 1
            Op.value.value.operand3.vr = sr_to_vr[Op.value.value.operand3.sr]
            Op.value.value.operand3.nu = lu[Op.value.value.operand3.sr]
            sr_to_vr[Op.value.value.operand3.sr] = None
            lu[Op.value.value.operand3.sr] = None

            if sr_to_vr[Op.value.value.operand1.sr] is None:
                sr_to_vr[Op.value.value.operand1.sr] = vr_name
                vr_name += 1
                cur_live = cur_live + 1
            Op.value.value.operand1.vr = sr_to_vr[Op.value.value.operand1.sr]
            Op.value.value.operand1.nu = lu[Op.value.value.operand1.sr]
            lu[Op.value.value.operand1.sr] = index

        elif Op.value.value.op == 'store':
            if sr_to_vr[Op.value.value.operand1.sr] is None:
                sr_to_vr[Op.value.value.operand1.sr] = vr_name
                vr_name += 1
                cur_live = cur_live + 1
            Op.value.value.operand1.vr = sr_to_vr[Op.value.value.operand1.sr]
            Op.value.value.operand1.nu = lu[Op.value.value.operand1.sr]
            lu[Op.value.value.operand1.sr] = index

            if sr_to_vr[Op.value.value.operand3.sr] is None:
                sr_to_vr[Op.value.value.operand3.sr] = vr_name
                vr_name += 1
                cur_live = cur_live + 1
            Op.value.value.operand3.vr = sr_to_vr[Op.value.value.operand3.sr]
            Op.value.value.operand3.nu = lu[Op.value.value.operand3.sr]
            lu[Op.value.value.operand3.sr] = index

        elif Op.value.value.op == "loadI":
            if sr_to_vr[Op.value.value.operand3.sr] is None:
                sr_to_vr[Op.value.value.operand3.sr] = vr_name
                vr_name += 1
            else:
                cur_live = cur_live - 1
            Op.value.value.operand3.vr = sr_to_vr[Op.value.value.operand3.sr]
            Op.value.value.operand3.nu = lu[Op.value.value.operand3.sr]
            sr_to_vr[Op.value.value.operand3.sr] = None
            lu[Op.value.value.operand3.sr] = None
        index = index - 1
        max_live = max(max_live, cur_live)
        Op = Op.prev


    IR.max_live = max_live
    IR.max_vr = vr_name

