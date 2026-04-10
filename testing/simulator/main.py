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
  "00000":  [0],
  "00010":  [0],
  "00001":  [0],
  "00011":  [0],
  "00100":  [0],
  "00101":  [0],
  "00110":  [0],
  "00111":  [0],
  "01000":  [0],
  "01001":  [0],
  "01010":  [0],
  "01011":  [0],
  "01100":  [0],
  "01101":  [0],
  "01110":  [0],
  "01111":  [0],
  "10000":  [0],
  "10001":  [0],
  "10010":  [0],
  "10011":  [0],
  "10100":  [0],
  "10101":  [0],
  "10110":  [0],
  "10111":  [0],
  "11000":  [0],
  "11001":  [0],
  "11010":  [0],
  "11011":  [0],
  "11100":  [0],
  "11101":  [0],
  "11110":  [0],
  "11111":  [0],
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
            print("add",Registers[rd])
        elif funct3 == "000" and funct7 == "0100000":  # sub
            Registers[rd] = [rs1_val - rs2_val]
            print("sub",Registers[rd])
        elif funct3 == "100" and funct7 == "0000000":  # xor
            Registers[rd] = [rs1_val ^ rs2_val]
            print("xor",Registers[rd])
        elif funct3 == "110" and funct7 == "0000000":  # or
            Registers[rd] = [rs1_val | rs2_val]
            print("or",Registers[rd])
        elif funct3 == "111" and funct7 == "0000000":  # and
            Registers[rd] = [rs1_val & rs2_val]
            print("and",Registers[rd])
        elif funct3 == "001" and funct7 == "0000000":  # sll
            temp = rs2_val & 0x1F
            Registers[rd] = [rs1_val << temp]
            print("sll",Registers[rd])
        elif funct3 == "101" and funct7 == "0000000":  # srl
            temp = rs2_val & 0x1F
            Registers[rd] = [(rs1_val & 0xFFFFFFFF) >> temp]  # logical shift
            print("srl",Registers[rd])
        elif funct3 == "101" and funct7 == "0100000":  # sra
            temp = rs2_val & 0x1F
            Registers[rd] = [rs1_val >> temp]  # arithmetic shift (Python preserves sign)
            print("sra",Registers[rd])
        elif funct3 == "010" and funct7 == "0000000":  # slt
            Registers[rd] = [1 if rs1_val < rs2_val else 0]
            print("slt",Registers[rd])
        elif funct3 == "011" and funct7 == "0000000":  # sltu
            Registers[rd] = [1 if (rs1_val & 0xFFFFFFFF) < (rs2_val & 0xFFFFFFFF) else 0]
            print("sltu",Registers[rd])

    except (ValueError, IndexError, KeyError) as error:
        print(f"Error processing R-type instruction: {instruction}. Error: {error}")
    
def I_TYPE_INSTRUCTION(instruction):#added try except
    try:
        if   instruction[25:32]=="0000011" and instruction[17:20]=="010":#"lw"   
             print(instruction)
        elif instruction[25:32]=="0010011" and instruction[17:20]=="000":#"addi" 
             print(instruction)
        elif instruction[25:32]=="0010011" and instruction[17:20]=="011":#"sltiu"
             print(instruction)
        elif instruction[25:32]=="1100111" and instruction[17:20]=="000":#"jalr" 
             print(instruction)

        
        # write_to_file(instruction,output_path,readable_path)
    except (ValueError,IndexError,KeyError) as error:
        st= f"Error processing instruction: {instruction}. Error: {error}"
        binary_instructions.append(st)

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
  
def main():
    x = input("file path ? ")
    # if len(sys.argv) < 3:
    #     print("error please provide this format :   python3 Assembler.py <input_assembly_path> <output_machine_code_path> [output_readable_path] ")
    #     return
    # x = sys.argv[1]
    try:
        with open(x, 'r') as file:
            for line in file:
                line=line.strip()
                instructions.append(line)
        print("-->",instructions,len(instructions))
    except FileNotFoundError:
        print("File not found.")
        exit()
        return
    for i in instructions:
        segrigator(i)
    # labels={}
    # collect_labels(instructions, labels)
    # pc_list=[]
    # pc=0
    # virtual_halt_count=0
    # if virtual_halt_count ==0:
    #     st=f"Error: No virtual halt instruction found.Use'beq zero, zero, 0'"
    #     binary_instructions.append(st)

main()
# output_path = sys.argv[2]
# if len(sys.argv) > 3:
#     readable_path = sys.argv[3]
# else:
#     readable_path=None


# write_to_file(instruction,output_path,readable_path)











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
