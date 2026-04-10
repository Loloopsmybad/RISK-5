import re 
import sys
import os
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
Registers = {#32 registers and their list
  "x0" :   [0],
  "x1" :  [0],
  "x2" :  [0],
  "x3" :  [0],
  "x4" :  [0],
  "x5" :  [0],
  "x6" :  [0],
  "x7" :  [0],
  "x8" :  [0],
  "x9" :  [0],
  "x10":  [0],
  "x11":  [0],
  "x12":  [0],
  "x13":  [0],
  "x14":  [0],
  "x15":  [0],
  "x16":  [0],
  "x17":  [0],
  "x18":  [0],
  "x19":  [0],
  "x20":  [0],
  "x21":  [0],
  "x22":  [0],
  "x23":  [0],
  "x24":  [0],
  "x25":  [0],
  "x26":  [0],
  "x27":  [0],
  "x28":  [0],
  "x29":  [0],
  "x30":  [0],
  "x31":  [0],
}
# PLEASE REFER THIS INDEX ENCODING 
# [0:7]   = funct7
# [7:12]  = rs2
# [12:17] = rs1
# [17:20] = funct3
# [20:25] = rd
# [25:32] = opcode

memory = {}
output_lines=[]
#helper functions
def to_u32(v):
    return v & 0xFFFFFFFF
def to_s32(v):
    v=to_u32(v)
    return v-0x100000000 if v>=0x80000000 else v
def sign_extend(v,bits):
    if(v>=(2**(bits-1))):
        v-=(1**bits)
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
    return memory.get(addr&-4,0)
def mem_store(addr,val):
    memory[addr&-4]=to_s32(val)
  
instructions=[]
def write_registers():
    a=[]
    for i in Registers:
        a.append(f"{i} : {(bin(Registers[i][0])[2:]).zfill(5)}")
    write_to_file(a,output_path,readable_path)
    
def segrigator(instruction):
    if   instruction[25:32]=="0110011":
        print("R-TYPE INSTRUCTION",instruction)
        R_TYPE_INSTRUCTION(instruction)
    elif instruction[25:32]in ["0000011","0010011","0010011","1100111"]:
        print("I-TYPE INSTRUCTION",instruction)
        I_TYPE_INSTRUCTION(instruction)
    elif instruction[25:32]=="0100011":
        print("S-TYPE INSTRUCTION",instruction)
        S_TYPE_INSTRUCTION(instruction)
    # elif instruction[32-6:32]=="1100011":
    #      print("B-TYPE INSTRUCTION",instruction)
    #      B_TYPE_INSTRUCTION(instruction)
    elif instruction[32-6:32]in["0110111","0010111"]:
         print("U-TYPE INSTRUCTION",instruction)
         U_TYPE_INSTRUCTION(instruction)
    # elif instruction[32-6:32]=="1101111":
    #     print("J-TYPE INSTRUCTION",instruction)
    #     J_TYPE_INSTRUCTION(instruction)

def write_to_file(instruction,output_file_path_name,readable_path=None):
    folder = os.path.dirname(output_file_path_name)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(output_file_path_name, 'a') as file:
            file.write(instruction + '\n')
    print(f"Binary instructions written to '{output_file_path_name}'")
    if readable_path:
        folder = os.path.dirname(readable_path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(readable_path, 'w') as file:
                file.write(instruction + '\n')
        print(f"Readable output written to '{readable_path}'")
    
def collect_labels(refined_instructions,labels):
    pc=0
    for inst in instructions:
        if inst[0].endswith(":"):
            label=inst[0][:-1]#remove colon
            labels[label]=pc
            if len(inst)>1:
                pc+=4
        else:
            pc+=4

def R_TYPE_INSTRUCTION(instruction):
    try:
        funct7 = instruction[0:7]
        funct3 = instruction[17:20] 
        rd     = instruction[20:25]
        rs2    = instruction[7:12]
        rs1    = instruction[12:17]
        
        rs1_val = Registers[rs1][0]
        rs2_val = Registers[rs2][0] 

        if   funct3 == "000" and funct7 == "0000000":  # add
            Registers[rd] = [rs1_val + rs2_val]
            write_registers()
        elif funct3 == "000" and funct7 == "0100000":  # sub
            Registers[rd] = [rs1_val - rs2_val]
            print("sub",Registers[rd])
            write_registers()
        elif funct3 == "100" and funct7 == "0000000":  # xor
            Registers[rd] = [rs1_val ^ rs2_val]
            print("xor",Registers[rd])
            write_registers()
        elif funct3 == "110" and funct7 == "0000000":  # or
            Registers[rd] = [rs1_val | rs2_val]
            print("or",Registers[rd])
            write_registers()
        elif funct3 == "111" and funct7 == "0000000":  # and
            Registers[rd] = [rs1_val & rs2_val]
            print("and",Registers[rd])
            write_registers()
        elif funct3 == "001" and funct7 == "0000000":  # sll
            temp = rs2_val & 0x1F
            Registers[rd] = [rs1_val << temp]
            print("sll",Registers[rd])
            write_registers()
        elif funct3 == "101" and funct7 == "0000000":  # srl
            temp = rs2_val & 0x1F
            Registers[rd] = [(rs1_val & 0xFFFFFFFF) >> temp]  # logical shift
            print("srl",Registers[rd])
            write_registers()
        elif funct3 == "101" and funct7 == "0100000":  # sra
            temp = rs2_val & 0x1F
            Registers[rd] = [rs1_val >> temp]  # arithmetic shift (Python preserves sign)
            print("sra",Registers[rd])
            write_registers()
        elif funct3 == "010" and funct7 == "0000000":  # slt
            Registers[rd] = [1 if rs1_val < rs2_val else 0]
            print("slt",Registers[rd])
            write_registers()
        elif funct3 == "011" and funct7 == "0000000":  # sltu
            Registers[rd] = [1 if (rs1_val & 0xFFFFFFFF) < (rs2_val & 0xFFFFFFFF) else 0]
            print("sltu",Registers[rd])
            write_registers()

    except (ValueError, IndexError, KeyError) as error:
        print(f"Error processing R-type instruction: {instruction}. Error: {error}")
    
def I_TYPE_INSTRUCTION(instruction, memory=None, pc=None):
    try:
                  
        rd       = instruction[20:25]
        rs1      = instruction[12:17]
        funct3   = instruction[17:20]
        opcode   = instruction[25:32]

        rs1_val  = Registers[rs1][0]
        imm_bits = instruction[0:12] # 12-bit immediate

        # sign-extend the 12-bit immediate
        imm = int(imm_bits, 2)
        if imm_bits[0] == "1":               # MSB set → negative
            imm -= (1 << 12)

        if   opcode == "0000011" and funct3 == "010":  # lw
             address = rs1_val + imm
             if memory is not None and address in memory:
                 Registers[rd] = [memory[address]]
                 print("lw",Registers[rd])
                 write_registers()
             else:
                 print(f"lw: memory address{address} not found") 
        elif opcode == "0010011" and funct3 == "000":  # addi
             Registers[rd] = [rs1_val + imm]
             print("addi",Registers[rd])
             write_registers()
        elif opcode == "0010011" and funct3 == "011":  # sltiu
             Registers[rd] = [1 if (rs1_val & 0xFFFFFFFF)<(imm & 0xFFFFFFFF) else 0]
             print("sltiu",Registers[rd])
             write_registers()
        elif opcode == "1100111" and funct3 == "000":  # jalr
             # rd = PC + 4, then jump to (rs1 + imm) & ~1
             if pc is not None:
                 Registers[rd] = [pc + 4]
             target = (rs1_val + imm) & ~1
             print("jalr", f"target={target}", Registers[rd])
             write_registers()
             return target                    # caller should update PC
    except (ValueError, IndexError, KeyError) as error:
        print(f"error processing Itype instruction:{instruction}.Error:{error}")

def S_TYPE_INSTRUCTION(instruction,pc):# added try except
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
        #write_to_file(instruction,output_path,readable_path)
    except (ValueError,IndexError,KeyError) as error:
        st= f"Error processing instruction: {instruction}. Error: {error}"
        binary_instructions.append(st)
        return pc + 4, False

def B_TYPE_INSTRUCTION(instruction,current_pc,labels):# added try except
    try:
        if   instruction[17:20]=="000":#"beq" 
             print(instruction)
        elif instruction[17:20]=="001":#"bne" 
             print(instruction)
        elif instruction[17:20]=="100":#"blt" 
             print(instruction)
        elif instruction[17:20]=="101":#"bge" 
             print(instruction)
        elif instruction[17:20]=="110":#"bltu"
             print(instruction)
        elif instruction[17:20]=="111":#"bgeu"
             print(instruction)


        
        # write_to_file(instruction,output_path,readable_path)
    except (ValueError,IndexError,KeyError) as error:
        st= f"Error processing instruction: {instruction}. Error: {error}"
        binary_instructions.append(st)
def sign_extend(binary_str):
    bits=len(binary_str)
    value=int(binary_str, 2)
    if binary_str[0]=='1':  
        value-=(1 << bits)
    return value
def bin_to_signed(val):
    val &=0xFFFFFFFF
    if val & 0x80000000:
        return val - 0x100000000
    return val
def btype_imm(instr):
   
    imm12=instr[0]         
    imm10_5=instr[1:7]     
    imm4_1=instr[20:24]    
    imm11=instr[24]       

    imm_bin=imm12+imm11+imm10_5+imm4_1+"0"
    return sign_extend(imm_bin)
def simulate_b_type(instr, pc,registers):

    if len(instr)!=32 or any(c not in '01' for c in instr):
        raise ValueError("Instruction must be a 32-bit binary string")
    opcode = instr[25:32]
    if opcode!="1100011":
        raise ValueError("Not a B-type instruction")
    funct3=instr[17:20]
    rs1=int(instr[12:17], 2)
    rs2=int(instr[7:12], 2)
    imm=btype_imm(instr)
    
    val1_unsigned=registers[rs1] & 0xFFFFFFFF
    val2_unsigned=registers[rs2] & 0xFFFFFFFF

    val1_signed=bin_to_signed(registers[rs1])
    val2_signed =bin_to_signed(registers[rs2])
    
    taken=False
    branch_name=""
    if funct3=="000":     
        branch_name="beq"
        taken=(val1_signed==val2_signed)

    elif funct3=="001":    
        branch_name="bne"
        taken=(val1_signed!=val2_signed)

    elif funct3=="100":   
        branch_name="blt"
        taken=(val1_signed < val2_signed)

    elif funct3 == "101":   
        branch_name = "bge"
        taken = (val1_signed >= val2_signed)

    elif funct3=="110":   
        branch_name ="bltu"
        taken=(val1_unsigned < val2_unsigned)

    elif funct3=="111":    
        branch_name ="bgeu"
        taken=(val1_unsigned >= val2_unsigned)

    else:
        raise ValueError("Invalid B-type funct3")

    if taken:
        new_pc=pc + imm
    else:
        new_pc=pc + 4
    if new_pc % 4 != 0:
        raise ValueError("Misaligned PC")
    registers[0]=0

    output=(
        f"PC={pc} | {branch_name} x{rs1}, x{rs2}, imm={imm} | "
        f"x{rs1}={registers[rs1]}, x{rs2}={registers[rs2]} | "
        f"taken={taken} | new_PC={new_pc}"
    )
    return new_pc, output
def run_btype_simulator(input_file, output_file):
    registers=[0] * 32
    
    registers[1]=10
    registers[2]=10
    registers[3]=5
    registers[4]=20

    pc=0
    outputs=[]
    with open(input_file, "r") as f:
        instructions=[line.strip() for line in f if line.strip()]

    for instr in instructions:
        try:
            opcode=instr[25:32]

            if opcode=="1100011":   
                pc, out=simulate_b_type(instr, pc, registers)
                outputs.append(out)
            else:
                outputs.append(f"PC={pc} | Not B-type, skipped")
                pc+=4
            registers[0]=0
        except Exception as e:
            outputs.append(f"PC={pc} | ERROR: {str(e)}")
            pc+=4

    with open(output_file, "w") as f:
        for line in outputs:
            f.write(line + "\n")

def U_TYPE_INSTRUCTION(instruction):# added try except
    try:
        opc=instruction[25:32]
        rd =instruction[20:25]
        imm=int(instruction[0:20],2)
        if(opc=="0110111"):#lui
            r=to_s32(imm<<12)
            write_reg(rd, r)
            print("lui rd=",rd,"=",hex(to_u32(r)))
        elif opc == "0010111":#auipc
            r=to_s32(pc+(imm<<12))
            write_reg(rd,r)
            print("auipc rd=",rd,"=",hex(to_u32(r)))
        return pc + 4, False
        # write_to_file(instruction,output_path,readable_path)
    except (ValueError,IndexError,KeyError) as error:
        st= f"Error processing instruction: {instruction}. Error: {error}"
        binary_instructions.append(st)
        return pc + 4, False

def J_TYPE_INSTRUCTION(instruction,labels,current_pc): # added try except
    try:
        if instruction[25:32]=="1101111":#"jal" 
             print(instruction)

        write_to_file(instruction,output_path,readable_path)
    except (ValueError,IndexError,KeyError) as error:
        st= f"Error processing instruction: {instruction}. Error: {error}"
        instructions.append(st)

def virtual_halt(instruction):
    if len(instruction)<4:
        return 0
    if(instruction[0]=="beq" and instruction[1]=="zero" and instruction[2]=="zero" and instruction[3]=="0"):
        return 1
    return 0
  
pc = 0
def PC(memory=None):
    global pc
    pc = 0
    while pc // 4 < len(instructions):
        instruction = instructions[pc // 4]
        opcode = instruction[25:32]

        if   opcode == "0110011":          # R-type
            R_TYPE_INSTRUCTION(instruction)
            pc += 4

        elif opcode in ["0000011", "0010011", "1100111"]:  # I-type
            result = I_TYPE_INSTRUCTION(instruction, memory=memory, pc=pc)
            if opcode == "1100111":        # jalr returns a target PC
                pc = result if result is not None else pc + 4
            else:
                pc += 4

        elif opcode == "0100011":          # S-type
            S_TYPE_INSTRUCTION(instruction)
            pc += 4

        elif opcode == "1100011":          # B-type
            offset = B_TYPE_INSTRUCTION(instruction, current_pc=pc, labels=labels)
            if offset is not None:
                pc += offset              # branch taken: pc += sign-extended offset
            else:
                pc += 4                   # branch not taken

        elif opcode in ["0110111", "0010111"]:  # U-type
            U_TYPE_INSTRUCTION(instruction)
            pc += 4

        elif opcode == "1101111":          # J-type (jal)
            target = J_TYPE_INSTRUCTION(instruction, labels=labels, current_pc=pc)
            pc = target if target is not None else pc + 4

        else:
            print(f"Unknown opcode: {opcode} at pc={pc}")
            pc += 4
def main():
    x = input("file path ? ")
    if len(sys.argv) < 3:
        print("error please provide this format :   python3 Simulator.py <input_machine_code_path> <output_trace_path> [output_readable_path] ")
        return
    global labels
    try:
        with open(x, 'r') as file:
            for line in file:
                instructions.append(line.strip())
    except FileNotFoundError:
        print("File not found.")
        return

    for i in instructions:
        segrigator(i)

    labels = {}
    collect_labels(instructions, labels)

    pc_list = []
    pc = 0
    virtual_halt_count = 0
    if virtual_halt_count == 0:
        st = f"Error: No virtual halt instruction found. Use 'beq zero, zero, 0'"
        binary_instructions.append(st)

    memory = {}
    PC(memory=memory)


main()
output_path = sys.argv[2]
if len(sys.argv) > 3:
    readable_path = sys.argv[3]
else:
    readable_path=None


write_to_file(instruction,output_path,readable_path)











#=================================FOR REFERENCE=================================================

#                          R_type_INSTRUCTIONS={
#                           #instruction   #opcode   #func3  #func 7
#                               "add"  : ["0110011", "000", "0000000"],
#                               "sub"  : ["0110011", "000", "0100000"],
#                               "xor"  : ["0110011", "100", "0000000"],
#                               "or"   : ["0110011", "110", "0000000"],
#                               "and"  : ["0110011", "111", "0000000"],
#                               "sll"  : ["0110011", "001", "0000000"],
#                               "srl"  : ["0110011", "101", "0000000"],
#                               "slt"  : ["0110011", "010", "0000000"],
#                               "sltu" : ["0110011", "011", "0000000"]
#                           }
#                           I_type_INSTRUCTIONS={
#                           # instruction   #opcode   #func3   #func7 (not used in I-type)
#                               "lw"    : ["0000011", "010", None],
#                               "addi"  : ["0010011", "000", None],
#                               "sltiu" : ["0010011", "011", None],
#                               "jalr"  : ["1100111", "000", None],
#                           }
#                           S_type_INSTRUCTIONS={
#                           #instruction   #opcode   #func3
#                               "sw"   : ["0100011", "010"],
#                           }
#                           B_type_INSTRUCTIONS={
#                           #instruction  #opcode  #func3
#                               "beq" : ["1100011","000"],
#                               "bne" : ["1100011","001"],
#                               "blt" : ["1100011","100"],
#                               "bge" : ["1100011","101"],
#                               "bltu": ["1100011","110"],
#                               "bgeu": ["1100011","111"]
#                           }
#                           U_type_INSTRUCTIONS={
#                           #instruction   #opcode
#                               "lui"  : ["0110111"],
#                               "auipc": ["0010111"],
#                           }
#                           J_type_INSTRUCTIONS={
#                           #instruction   #opcode
#                               "jal"  : ["1101111"],
#                           }
