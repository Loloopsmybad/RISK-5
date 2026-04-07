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
  "00000":  [],
  "00010":  [],
  "00001":  [],
  "00011":  [],
  "00100":  [],
  "00101":  [],
  "00110":  [],
  "00111":  [],
  "01000":  [],
  "01001":  [],
  "01010":  [],
  "01011":  [],
  "01100":  [],
  "01101":  [],
  "01110":  [],
  "01111":  [],
  "10000":  [],
  "10001":  [],
  "10010":  [],
  "10011":  [],
  "10100":  [],
  "10101":  [],
  "10110":  [],
  "10111":  [],
  "11000":  [],
  "11001":  [],
  "11010":  [],
  "11011":  [],
  "11100":  [],
  "11101":  [],
  "11110":  [],
  "11111":  [],
}
R_type_INSTRUCTIONS={
#instruction   #opcode   #func3  #func 7
    "add"  : ["0110011", "000", "0000000"],
    "sub"  : ["0110011", "000", "0100000"],
    "xor"  : ["0110011", "100", "0000000"],
    "or"   : ["0110011", "110", "0000000"],
    "and"  : ["0110011", "111", "0000000"],
    "sll"  : ["0110011", "001", "0000000"],
    "srl"  : ["0110011", "101", "0000000"],
    "slt"  : ["0110011", "010", "0000000"],
    "sltu" : ["0110011", "011", "0000000"]
}
I_type_INSTRUCTIONS={
# instruction   #opcode   #func3   #func7 (not used in I-type)
    "lw"    : ["0000011", "010", None],
    "addi"  : ["0010011", "000", None],
    "sltiu" : ["0010011", "011", None],
    "jalr"  : ["1100111", "000", None],
}
S_type_INSTRUCTIONS={
#instruction   #opcode   #func3
    "sw"   : ["0100011", "010"],
}
B_type_INSTRUCTIONS={
#instruction  #opcode  #func3
    "beq": ["1100011","000"],
    "bne": ["1100011","001"],
    "blt": ["1100011","100"],
    "bge": ["1100011","101"],
    "bltu":["1100011","110"],
    "bgeu":["1100011","111"]
}
U_type_INSTRUCTIONS={
#instruction   #opcode
    "lui"  : ["0110111"],
    "auipc": ["0010111"],
}
J_type_INSTRUCTIONS={
#instruction   #opcode
    "jal"  : ["1101111"],
}
instructions=[]
def segrigator(instuction):
    if instruction[0:6]=="0110011":
         R_TYPE_INSTRUCTION(instruction)
    elif instruction[0:6]in ["0000011","0010011","0010011","1100111"]:
         I_TYPE_INSTRUCTION(instruction)
    elif instruction[0:6]in["1100011","1100011","1100011","1100011","1100011","1100011"]:
         S_TYPE_INSTRUCTION(instruction)
    elif instruction[0:6]=="1100011":
         B_TYPE_INSTRUCTION(instruction)
    elif instruction[0:6]in["0110111","0010111"]:
         U_TYPE_INSTRUCTION(instruction)
    elif instruction[0:6]=="1101111":
         J_TYPE_INSTRUCTION(instruction)

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
    for inst in refined_instructions:
        if inst[0].endswith(":"):
            label=inst[0][:-1]#remove colon
            labels[label]=pc
            if len(inst)>1:
                pc+=4
        else:
            pc+=4

def R_TYPE_INSTRUCTION(instruction):#added try except
    try:
        if   instruction[12:14]=="000" and instruction [25:31] =="0000000":
            print("lol")
        elif instruction[12:14]=="000" and instruction [25:31] =="0100000":
            print("lol")
        elif instruction[12:14]=="100" and instruction [25:31] =="0000000":
            print("lol")
        elif instruction[12:14]=="110" and instruction [25:31] =="0000000":
            print("lol")
        elif instruction[12:14]=="111" and instruction [25:31] =="0000000":
            print("lol")
        elif instruction[12:14]=="001" and instruction [25:31] =="0000000":
            print("lol")
        elif instruction[12:14]=="101" and instruction [25:31] =="0000000":
            print("lol")
        elif instruction[12:14]=="010" and instruction [25:31] =="0000000":
            print("lol")
        elif instruction[12:14]=="011" and instruction [25:31] =="0000000":
            print("lol")


        print(binary_instruction,"R TYPE")
        binary_instructions.append(binary_instruction)
    except (ValueError,IndexError,KeyError) as error:
        st= f"Error processing instruction: {instruction}. Error: {error}"
        binary_instructions.append(st)
    
def I_TYPE_INSTRUCTION(instruction):#added try except
    try:
        if   instruction[12:14]=="000" and instruction [25:31] =="0000000":
            print("lol")
        elif instruction[12:14]=="000" and instruction [25:31] =="0100000":
            print("lol")
        elif instruction[12:14]=="100" and instruction [25:31] =="0000000":
            print("lol")
        elif instruction[12:14]=="110" and instruction [25:31] =="0000000":
            print("lol")
            
        print(inst,"I TYPE")
        binary_instructions.append(inst)
    except (ValueError,IndexError,KeyError) as error:
        st= f"Error processing instruction: {instruction}. Error: {error}"
        binary_instructions.append(st)

def S_TYPE_INSTRUCTION(instruction):# added try except
    try:
        if   instruction[12:14]=="000" and instruction [25:31] =="0000000":
            print("lol")
            
        print(binary_s_instruction,"S TYPE")
        binary_instructions.append(binary_s_instruction)
    except (ValueError,IndexError,KeyError) as error:
        st= f"Error processing instruction: {instruction}. Error: {error}"
        binary_instructions.append(st)

def B_TYPE_INSTRUCTION(instruction,current_pc,labels):# added try except
    try:
        print(instruction,"B TYPE")  
        instructions.append(instruction)
    except (ValueError,IndexError,KeyError) as error:
        st= f"Error processing instruction: {instruction}. Error: {error}"
        binary_instructions.append(st)

def U_TYPE_INSTRUCTION(instruction):# added try except
    try:
        print(instruction, "U TYPE")
        instructions.append(instruction)
    except (ValueError,IndexError,KeyError) as error:
        st= f"Error processing instruction: {instruction}. Error: {error}"
        binary_instructions.append(st)

def J_TYPE_INSTRUCTION(instruction,labels,current_pc): # added try except
    try:
        print(instruction, "J TYPE")
        instructions.append(binary_j_instruction)
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
    # x = input("file path ? ")
    if len(sys.argv) < 3:
        print("error please provide this format :   python3 Assembler.py <input_assembly_path> <output_machine_code_path> [output_readable_path] ")
        return
    x = sys.argv[1]
    try:
        with open(x, 'r') as file:
            for line in file:
                line=line[::-1]
                instructions.append(line)
            print("-->",refined_instructions,len(refined_instructions))
    except FileNotFoundError:
        print("File not found.")
        exit()
        return

    labels={}
    collect_labels(refined_instructions, labels)
    pc_list=[]
    pc=0
    virtual_halt_count=0
    if virtual_halt_count ==0:
        st=f"Error: No virtual halt instruction found.Use'beq zero, zero, 0'"
        binary_instructions.append(st)


main()
output_path = sys.argv[2]
if len(sys.argv) > 3:
    readable_path = sys.argv[3]
else:
    readable_path=None


write_to_file(instruction,output_path,readable_path)