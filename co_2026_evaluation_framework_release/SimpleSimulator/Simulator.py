import re
import sys
import os
from collections import defaultdict

'''
note the ADRESSES ARE AS FFOLOWS

| Address                   | Register | ABI Name | Description                          | Saver  |
| 0000_0                    | x0       | zero     | Hard-wired zero                      | —      |
| 0000_1                    | x1       | ra       | Return address                       | Caller |
| 0001_0                    | x2       | sp       | Stack Pointer                        | Callee |
| 0001_1                    | x3       | gp       | Global Pointer                       | —      |
| 0010_0                    | x4       | tp       | Thread Pointer                       | —      |
| 0010_1                    | x5       | t0       | Temporary / alternate link register  | Caller |
| 00_{110,111}              | x6-7     | t1-2     | Temporaries                          | Caller |
| 0100_0                    | x8       | s0/fp    | Saved register / frame pointer       | Callee |
| 0100_1                    | x9       | s1       | Saved register                       | Callee |
| 0101_{0,1}                | x10-11   | a0-1     | Function arguments / return values   | Caller |
| (011_{00-11}),(1000_{0,1})| x12-17   | a2-7     | Function arguments                   | Caller |
| 1_{0010-1011}             | x18-27   | s2-11    | Saved registers                      | Caller |
| 111_{00-11}               | x28-31   | t3-6     | Temporaries                          | Caller |
'''

# Maps 5-bit binary string → register name e.g. "00000" → "x0"
BIN_TO_REG = {format(i, '05b'): f"x{i}" for i in range(32)}

Registers = {
    "x0" : [0], 
    "x1" : [0], 
    "x2" : [0], 
    "x3" : [0],
    "x4" : [0], 
    "x5" : [0], 
    "x6" : [0], 
    "x7" : [0],
    "x8" : [0], 
    "x9" : [0], 
    "x10": [0], 
    "x11": [0],
    "x12": [0], 
    "x13": [0], 
    "x14": [0], 
    "x15": [0],
    "x16": [0], 
    "x17": [0], 
    "x18": [0], 
    "x19": [0],
    "x20": [0], 
    "x21": [0], 
    "x22": [0], 
    "x23": [0],
    "x24": [0], 
    "x25": [0], 
    "x26": [0], 
    "x27": [0],
    "x28": [0], 
    "x29": [0], 
    "x30": [0], 
    "x31": [0],
}

# Data memory: 32 locations x 32-bit, base address 0x00010000
DATA_MEM_BASE = 0x00010000
memory = defaultdict(int)

# Stack memory: base 0x00000100, SP initialised to 0x0000017C
STACK_BASE   = 0x00000100
STACK_TOP    = 0x0000017C
Registers["x2"] = [STACK_TOP]   # sp = x2

# PLEASE REFER THIS INDEX ENCODING
# [0:7]   = funct7   (bits 31:25)
# [7:12]  = rs2      (bits 24:20)
# [12:17] = rs1      (bits 19:15)
# [17:20] = funct3   (bits 14:12)
# [20:25] = rd       (bits 11:7)
# [25:32] = opcode   (bits 6:0)

instructions   = []
output_path    = None
readable_path  = None
labels         = {}
pc             = 0
def bin_to_signed(val):
    val &= 0xFFFFFFFF
    if val & 0x80000000:
        return val - 0x100000000
    return val

def write_to_file(data, output_file_path_name, r_path=None):
    """Write a string or list of strings to the output file."""
    folder = os.path.dirname(output_file_path_name)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(output_file_path_name, 'a') as f:
        if isinstance(data, list):
            for line in data:
                f.write(str(line) + '\n')
        else:
            f.write(str(data) + '\n')
    if r_path:
        folder = os.path.dirname(r_path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(r_path, 'a') as f:
            if isinstance(data, list):
                for line in data:
                    f.write(str(line) +'\n')
            else:
                f.write(str(data)+'\n')

def write_registers(current_pc):
    pc_bin  = "0b" + bin(current_pc)[2:].zfill(32)
    reg_bin = " ".join("0b" + bin(Registers[f"x{i}"][0] & 0xFFFFFFFF)[2:].zfill(32)
                       for i in range(32))
    line = f"{pc_bin} {reg_bin}"
    if output_path:
        write_to_file(line, output_path)
    # print(line)

def write_memory():
    """
    Print memory after virtual halt:
    Address in hex:32-bit binary data
    """
    lines = []
    for i in range(32):
        addr = DATA_MEM_BASE + i * 4
        val  = memory.get(addr, 0)
        lines.append(f"0x{addr:08X}:0b{bin(val & 0xFFFFFFFF)[2:].zfill(32)}")
    if output_path:
        write_to_file(lines, output_path)
    # for l in lines:
    #     # print(l)

# def segrigator(instruction):
#     if   instruction[25:32] == "0110011":
#         print("R-TYPE INSTRUCTION", instruction)
#         R_TYPE_INSTRUCTION(instruction)
#     elif instruction[25:32] in ["0000011", "0010011", "1100111"]:
#         print("I-TYPE INSTRUCTION", instruction)
#         I_TYPE_INSTRUCTION(instruction)
#     elif instruction[25:32] == "0100011":
#         print("S-TYPE INSTRUCTION", instruction)
#         S_TYPE_INSTRUCTION(instruction)
#     elif instruction[25:32] == "1100011":
#         print("B-TYPE INSTRUCTION", instruction)
#         B_TYPE_INSTRUCTION(instruction, current_pc=pc, labels=labels)
#     elif instruction[25:32] in ["0110111", "0010111"]:
#         print("U-TYPE INSTRUCTION", instruction)
#         U_TYPE_INSTRUCTION(instruction)
#     elif instruction[25:32] == "1101111":
#         print("J-TYPE INSTRUCTION", instruction)
#         J_TYPE_INSTRUCTION(instruction, labels=labels, current_pc=pc)

#helper functiom
def to_u32(v):
    return v & 0xFFFFFFFF
def to_s32(v):
    v=to_u32(v)
    return v-0x100000000 if v>=0x80000000 else v
def sign_extend(v,bits):
    if(v>=(2**(bits-1))):
        v-=(2**bits)
    return v
def bin32(v):
    return format(to_u32(v),'032b')
def read_reg(key):
    if(key=="00000"):
        return 0
    return Registers[key][0]
def write_reg(key, val):
    if(key=="00000"):
        return
    Registers[key][0]=to_s32(val)
def mem_load(addr):
    return memory.get(addr & -4, 0)
def mem_store(addr, val):
    memory[addr & -4] = to_s32(val)
    
def R_TYPE_INSTRUCTION(instruction):
    try:
        funct7  = instruction[0:7]
        rs2     = BIN_TO_REG[instruction[7:12]]
        rs1     = BIN_TO_REG[instruction[12:17]]
        funct3  = instruction[17:20]
        rd      = BIN_TO_REG[instruction[20:25]]

        rs1_val = Registers[rs1][0]
        rs2_val = Registers[rs2][0]

        if   funct3 == "000" and funct7 == "0000000":  # add
            Registers[rd] = [rs1_val + rs2_val]
            # print("add", Registers[rd])
        elif funct3 == "000" and funct7 == "0100000":  # sub
            Registers[rd] = [rs1_val - rs2_val]
            # print("sub", Registers[rd])
        elif funct3 == "100" and funct7 == "0000000":  # xor
            Registers[rd] = [rs1_val ^ rs2_val]
            # print("xor", Registers[rd])
        elif funct3 == "110" and funct7 == "0000000":  # or
            Registers[rd] = [rs1_val | rs2_val]
            # print("or", Registers[rd])
        elif funct3 == "111" and funct7 == "0000000":  # and
            Registers[rd] = [rs1_val & rs2_val]
            # print("and", Registers[rd])
        elif funct3 == "001" and funct7 == "0000000":  # sll
            shamt = rs2_val & 0x1F
            Registers[rd] = [rs1_val << shamt]
            # print("sll", Registers[rd])
        elif funct3 == "101" and funct7 == "0000000":  # srl
            shamt = rs2_val & 0x1F
            Registers[rd] = [(rs1_val & 0xFFFFFFFF) >> shamt]
            # print("srl", Registers[rd])
        elif funct3 == "101" and funct7 == "0100000":  # sra
            shamt = rs2_val & 0x1F
            Registers[rd] = [rs1_val >> shamt]
            # print("sra", Registers[rd])
        elif funct3 == "010" and funct7 == "0000000":  # slt
            Registers[rd] = [1 if rs1_val < rs2_val else 0]
            # print("slt", Registers[rd])
        elif funct3 == "011" and funct7 == "0000000":  # sltu
            Registers[rd] = [1 if (rs1_val & 0xFFFFFFFF) < (rs2_val & 0xFFFFFFFF) else 0]
            # print("sltu", Registers[rd])

        Registers["x0"] = [0]   # x0 is always 0

    except (ValueError, IndexError, KeyError) as error:
        print(f"Error R-type: {instruction}. Error: {error}")

def I_TYPE_INSTRUCTION(instruction, current_pc=None):
    try:
        imm_bits = instruction[0:12]          # bits [31:20]
        rs1      = BIN_TO_REG[instruction[12:17]]
        funct3   = instruction[17:20]
        rd       = BIN_TO_REG[instruction[20:25]]
        opcode   = instruction[25:32]

        rs1_val  = Registers[rs1][0]

        # sign-extend 12-bit immediate
        imm = int(imm_bits, 2)
        if imm_bits[0] == "1":
            imm -= (1 << 12)

        if  opcode == "0000011" and funct3 == "010":# lw
            address = rs1_val + imm
            Registers[rd] = [memory[address]]
            # print("lw",Registers[rd])

        elif opcode == "0010011" and funct3 == "000":#addi
            Registers[rd] = [rs1_val + imm]
            # print("addi",Registers[rd])

        elif opcode == "0010011" and funct3 == "011":#sltiu
            Registers[rd] = [1 if (rs1_val & 0xFFFFFFFF) < (imm & 0xFFFFFFFF) else 0]
            # print("sltiu",Registers[rd])

        elif opcode == "1100111" and funct3 == "000":#jalr
            if current_pc is not None:
                Registers[rd] = [current_pc + 4]
            target = (rs1_val + imm) & ~1     # clear LSB
            # print("jalr", f"target={target}",Registers[rd])
            Registers["x0"] = [0]
            return target                     

        Registers["x0"] = [0]

    except (ValueError, IndexError, KeyError) as error:
        print(f"Error I-type: {instruction}. Error: {error}")

def S_TYPE_INSTRUCTION(instruction,pc):
    try:
        rs2 =instruction[7:12]
        rs1 =instruction[12:17]
        f3  =instruction[17:20]
        imm =sign_extend(int(instruction[0:7]+instruction[20:25],2),12)#join both parts of imm
        if(f3=="010"):
            addr =to_u32(read_reg(rs1)+imm)
            val=read_reg(rs2)
            mem_store(addr,val)
        else:
            print(f"Error: Unknown S-type f3={f3}")
        return pc + 4, False

    except (ValueError, IndexError, KeyError) as error:
        print(f"Error in S-TYPE: {instruction} → {error}")
        return pc + 4, False

def B_TYPE_INSTRUCTION(instruction, current_pc=0, labels={}):
    try:
        # Reconstruct B-type immediate: imm[12]|imm[11]|imm[10:5]|imm[4:1]|0
        # instruction[0] is bit 31 (imm[12])
        # instruction[24] is bit 7 (imm[11])
        # instruction[1:7] is bits 30:25 (imm[10:5])
        # instruction[20:24] is bits 11:8 (imm[4:1])
        imm_bits = (instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24] + '0')

        rs1_idx = BIN_TO_REG[instruction[12:17]]
        rs2_idx = BIN_TO_REG[instruction[7:12]]
        funct3 = instruction[17:20]

        # Get values from your Registers dictionary
        val1_raw = Registers[rs1_idx][0]
        val2_raw = Registers[rs2_idx][0]

        # Prepare signed values for signed comparisons
        val1_signed = bin_to_signed(val1_raw)
        val2_signed = bin_to_signed(val2_raw)
        
        # Prepare unsigned values (32-bit mask)
        val1_unsigned = val1_raw & 0xFFFFFFFF
        val2_unsigned = val2_raw & 0xFFFFFFFF

        # Parse the immediate string to an integer
        imm = int(imm_bits, 2)
        if imm_bits[0] == "1": # Sign extend 13-bit immediate
            imm -= (1 << 13)

        taken = False
        if funct3 == "000":    # beq
            taken = (val1_signed == val2_signed)
        elif funct3 == "001":  # bne
            taken = (val1_signed != val2_signed)
        elif funct3 == "100":  # blt
            taken = (val1_signed < val2_signed)
        elif funct3 == "101":  # bge
            taken = (val1_signed >= val2_signed)
        elif funct3 == "110":  # bltu
            taken = (val1_unsigned < val2_unsigned)
        elif funct3 == "111":  # bgeu
            taken = (val1_unsigned >= val2_unsigned)

        Registers["x0"] = [0]
        
        # Return the offset if branch is taken, otherwise return 4 (standard increment)
        if taken:
            return imm 
        else:
            return 4  # Note: I changed this from None to 4 for easier handling in PC_run

    except (ValueError, IndexError, KeyError) as error:
        print(f"Error B-type: {instruction}. Error: {error}")
        return 

def U_TYPE_INSTRUCTION(instruction,pc):
    try:
        opc=instruction[25:32]
        rd =instruction[20:25]
        imm=int(instruction[0:20],2)

        if(opc=="0110111"):#lui
            r=to_s32(imm<<12)
            write_reg(rd, r)
        elif opc == "0010111":#auipc
            r=to_s32(pc+(imm<<12))
            write_reg(rd,r)
        return pc + 4, False

    except (ValueError, IndexError, KeyError) as error:
        print(f"Error in U-TYPE: {instruction} → {error}")
        return pc + 4, False

def J_TYPE_INSTRUCTION(instruction, pc):
    try:
        rd  = instruction[20:25]
        imm = sign_extend(
            int(instruction[0]+instruction[12:20]+instruction[11]+instruction[1:11]+"0",2),21)
        target = (to_u32(pc+imm)&-2)
        write_reg(rd, pc + 4)
        return target, False
    
    except (ValueError, IndexError, KeyError) as error:
        print(f"Error Jtype: {instruction} Error: {error}")
        return pc + 4, False

def virtual_halt(instruction):
    """beq zero, zero, 0  →  opcode=1100011, funct3=000, rs1=x0, rs2=x0, imm=0"""
    if len(instruction) < 32:
        return False
    if not (instruction[25:32] == "1100011" and   # opcode: beq
            instruction[17:20] == "000"      and   # funct3
            instruction[12:17] == "00000"    and   # rs1 = zero
            instruction[7:12]  == "00000"):        # rs2 = zero
        return False
    # Also verify the immediate offset is 0 (not just any beq x0,x0,offset)
    imm_bits = instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24] + '0'
    imm = int(imm_bits, 2)
    if imm_bits[0] == "1":
        imm -= (1 << 13)
    return imm == 0

def PC_run():
    global pc
    pc = 0
    # Clear output files before writing (avoid stale append from previous run)
    if output_path and os.path.exists(output_path):
        os.remove(output_path)
    if readable_path and os.path.exists(readable_path):
        os.remove(readable_path)

    while pc // 4 < len(instructions):
        instruction = instructions[pc // 4]
        opcode = instruction[25:32]

        #virtual halt 
        if virtual_halt(instruction):
            print("VIRTUAL HALT — stopping execution")
            write_registers(pc)
            write_memory()
            return
        #R type 
        if opcode == "0110011":
            R_TYPE_INSTRUCTION(instruction)
            pc += 4
            write_registers(pc)
        #Itype 
        elif opcode in ["0000011", "0010011"]:
            I_TYPE_INSTRUCTION(instruction, current_pc=pc)
            pc += 4
            write_registers(pc)
        elif opcode == "1100111":                      # jalr
            target = I_TYPE_INSTRUCTION(instruction, current_pc=pc)
            pc = target if target is not None else pc + 4
            write_registers(pc)
        #stype 
        elif opcode == "0100011":
            S_TYPE_INSTRUCTION(instruction)
            pc += 4
            write_registers(pc)
        #btype 
        elif opcode == "1100011":
            offset = B_TYPE_INSTRUCTION(instruction, current_pc=pc, labels=labels)
            if offset is not None:
                pc += offset              # branch taken
            else:
                pc += 4
            write_registers(pc)
        #utype 
        elif opcode in ["0110111", "0010111"]:
            U_TYPE_INSTRUCTION(instruction, current_pc=pc)
            pc += 4
            write_registers(pc)
        #jtype
        elif opcode == "1101111":
            target = J_TYPE_INSTRUCTION(instruction, labels=labels, current_pc=pc)
            pc = target if target is not None else pc + 4
            write_registers(pc)

def main():
    global output_path
    global readable_path
    global labels
    global instructions
    global pc

    # Reset all global state for clean run
    instructions.clear()
    pc = 0
    for key in Registers:
        Registers[key] = [0]
    Registers["x2"] = [STACK_TOP]   # sp = x2
    memory.clear()

    if len(sys.argv) < 3:
        print("error please provide this format : python3 Simulator.py <input_machine_code_path> <output_trace_path> [output_readable_path]")
        return

    input_path   = sys.argv[1]
    output_path  = sys.argv[2]
    readable_path = sys.argv[3] if len(sys.argv) > 3 else None
    # input_path   = 'lol.txt'
    # output_path  = 'lol1.txt'
    # readable_path = input("readable path?")
    try:
        with open(input_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    instructions.append(line)
        # print("-->",instructions,len(instructions))
    except FileNotFoundError:
        print("file not found")
        return

    # for i in instructions:
    #     segrigator(i)

    virtual_halt_count = sum(1 for inst in instructions if virtual_halt(inst))
    if virtual_halt_count == 0:
        print("Error: No virtual halt instruction found Use 'beq zero zero, 0'")
        return

    PC_run()


main()
