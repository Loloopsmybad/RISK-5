import re 
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
Registers = {#32 registers and their 2nd name
  "zero":  "00000", "x0" :"00000",
    "ra":  "00001", "x1" :"00001",
    "sp":  "00010", "x2" :"00010",
    "gp":  "00011", "x3" :"00011",
    "tp":  "00100", "x4" :"00100",
    "t0":  "00101", "x5" :"00101",
    "t1":  "00110", "x6" :"00110",
    "t2":  "00111", "x7" :"00111",
    "s0":  "01000", "fp" :"01000", "x8": "01000",
    "s1":  "01001", "x9" :"01001",
    "a0":  "01010", "x10":"01010",
    "a1":  "01011", "x11":"01011",
    "a2":  "01100", "x12":"01100",
    "a3":  "01101", "x13":"01101",
    "a4":  "01110", "x14":"01110",
    "a5":  "01111", "x15":"01111",
    "a6":  "10000", "x16":"10000",
    "a7":  "10001", "x17":"10001",
    "s2":  "10010", "x18":"10010",
    "s3":  "10011", "x19":"10011",
    "s4":  "10100", "x20":"10100",
    "s5":  "10101", "x21":"10101",
    "s6":  "10110", "x22":"10110",
    "s7":  "10111", "x23":"10111",
    "s8":  "11000", "x24":"11000",
    "s9":  "11001", "x25":"11001",
    "s10": "11010", "x26":"11010",
    "s11": "11011", "x27":"11011",
    "t3":  "11100", "x28":"11100",
    "t4":  "11101", "x29":"11101",
    "t5":  "11110", "x30":"11110",
    "t6":  "11111", "x31":"11111",
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
    "sra"  : ["0110011", "101", "0100000"],
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
insbinary = []


def convert_binary(n, bits):
    n = int(n)
    if n < -(2**(bits-1)) or n > (2**(bits-1) - 1):
        print("Overflow occured")
        exit()
    if n < 0:
        n = 2**bits + n  

    binary = ""
    while n > 0:
        binary += str(n % 2)
        n = n // 2

    if binary == "":
        binary = "0"

    binary = binary[::-1]
    zeros = bits - len(binary)
    binary = "0"*zeros + binary

    return binary


def R_TYPE_INSTRUCTION(instruction):
    print("")
    print(instruction)
    binary_instruction=""
    binary_instruction=binary_instruction+(R_type_INSTRUCTIONS[instruction[0]][2])#func7
    binary_instruction=binary_instruction+(Registers[instruction[3]])#rs2
    binary_instruction=binary_instruction+(Registers[instruction[2]])#rs1
    binary_instruction=binary_instruction+(R_type_INSTRUCTIONS[instruction[0]][1])#func3
    binary_instruction=binary_instruction+(Registers[instruction[1]])#rd
    binary_instruction=binary_instruction+(R_type_INSTRUCTIONS[instruction[0]][0])#opcode
    print(binary_instruction)
    binary_instructions.append(binary_instruction)
    
def I_TYPE_INSTRUCTION(instruction):
    short = instruction[0]

    opcode = I_type_INSTRUCTIONS[short][0]
    func3  = I_type_INSTRUCTIONS[short][1]

    if short == "lw":
        rd  = Registers[instruction[1]]
        imm = convert_binary(instruction[2], 12)
        rs1 = Registers[instruction[3]]
    else:
        rd  = Registers[instruction[1]]
        rs1 = Registers[instruction[2]]
        imm = convert_binary(instruction[3], 12)

    inst = imm + rs1 + func3 + rd + opcode
    binary_instructions.append(inst)



def S_TYPE_INSTRUCTION(instruction):
    print("")
    print(instruction)
    subpart= instruction #break the instruction
    pre_process(subpart)
    print(subpart)
    operation = subpart[0]
    rs2id= subpart[1]
    imm_str= subpart[2]
    rs1id= subpart[3]

    opcode=S_type_INSTRUCTIONS[operation][0]
    func3=S_type_INSTRUCTIONS[operation][1]
    rs2= Registers[rs2id]
    rs1= Registers[rs1id]
    imm12bits= convert_imm(imm_str,12)
    immstart= imm12bits[0:7] #imm[11:5]
    immend= imm12bits[7:12] #imm[4:0]
    binary_s_instruction=immstart+rs2+rs1+func3+immend+opcode
    print(binary_s_instruction)
    binary_instructions.append(binary_s_instruction)
    # return binary_s_instruction

def B_TYPE_INSTRUCTION(instruction):
    print("")
    print("B_TYPE_INSTRUCTION")

def convert_binary(value, bits):
    binarystr=""
    while value>0:
        binarystr= str(value%2)+binarystr
        value=value//2
    if (int(bits)<len(binarystr)):
        print("Overflow")
    else:
        x=bits- len(binarystr)
        binarystr=str("0"*x)+binarystr
    binary_instructions.append(binarystr)
    # return binarystr

def U_TYPE_INSTRUCTION(instruction):
    print("")
    print(instruction)
    subpart= instruction #break the instruction
    pre_process(subpart)
    print(subpart)
    operation= subpart[0]
    rdid= subpart[1]
    imm_str=subpart[2]
    opcode=U_type_INSTRUCTIONS[operation][0] #find the value of opcode from dictionary
    rd= Registers[rdid]
    imm20bit= convert_imm(imm_str,20) #convert it into 20 bits

    binary_u_instruction= opcode+rd+imm20bit
    print(binary_u_instruction)
    binary_instructions.append(binary_u_instruction)
    # return binary_u_instruction

def J_TYPE_INSTRUCTION(instruction):  
    print("")
    print(instruction)
    subpart= instruction #break the instruction
    pre_process(subpart)
    print(subpart)

    operation= subpart[0]
    rdid= subpart[1]
    imm_str=subpart[2]
    opcode= J_type_INSTRUCTIONS[operation][0]
    rd=Registers[rdid]
    imm21bit=convert_imm(imm_str,21)
    signbit= imm21bit[0]#imm[20] represents sign of imm[19] which is also bit 31
    target= imm21bit[1:9]#imm[19:12]
    next=imm21bit[9]#imm[11]
    source= imm21bit[10:20]#imm[10:1]
    binary_j_instruction= signbit+source+next+target+rd+opcode
    print(binary_j_instruction)
    binary_instructions.append(binary_j_instruction)
    # return binary_j_instruction
  
def main():
    x = input("file path ? ")
    try:
        with open(x, 'r') as file:
            for line in file:
                if line.strip() != '':
                    line=line.replace("("," ")
                    line=line.replace(")"," ")
                    line=line.replace(","," ")
                    line=line.strip().split(" ")
                    # print(line)
                    pre_process(line)
                    # print(line)
                    refined_instructions.append(line)
            print(refined_instructions,len(refined_instructions))
    except FileNotFoundError:
        print("File not found.")
        return
    for i in range(len(refined_instructions)):
        # print(f"checking: {parts[0]}")
        if refined_instructions[i][0] in R_type_INSTRUCTIONS:
            R_TYPE_INSTRUCTION(refined_instructions[i])
        elif refined_instructions[i][0] in I_type_INSTRUCTIONS:
            I_TYPE_INSTRUCTION(refined_instructions[i])
        elif refined_instructions[i][0] in S_type_INSTRUCTIONS:
            S_TYPE_INSTRUCTION(refined_instructions[i])
        elif refined_instructions[i][0] in B_type_INSTRUCTIONS:
            B_TYPE_INSTRUCTION(refined_instructions[i])
        elif refined_instructions[i][0] in U_type_INSTRUCTIONS:
            U_TYPE_INSTRUCTION(refined_instructions[i])
        elif refined_instructions[i][0] in J_type_INSTRUCTIONS:
            J_TYPE_INSTRUCTION(refined_instructions[i])

    
main()
write_to_file()