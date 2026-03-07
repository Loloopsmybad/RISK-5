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
    "zero":"00000", "x0":"00000",
    "ra":  "00001", "x1":"00001",
    "sp":  "00010", "x2":"00010",
    "gp":  "00011", "x3":"00011",
    "tp":  "00100", "x4":"00100",
    "t0":  "00101", "x5":"00101",
    "t1":  "00110", "x6":"00110",
    "t2":  "00111", "x7":"00111",
    "s0":  "01000", "fp":"01000", "x8": "01000",
    "s1":  "01001", "x9": "01001",
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
    "sll"  : ["0110011", "001", "0000000"],
    "slt"  : ["0110011", "010", "0000000"],
    "sltu" : ["0110011", "011", "0000000"],
    "xor"  : ["0110011", "100", "0000000"],
    "srl"  : ["0110011", "101", "0000000"],
    "or"   : ["0110011", "110", "0000000"],
    "and"  : ["0110011", "111", "0000000"]
}
I_type_INSTRUCTIONS={
# instruction   #opcode   #func3   #func7 (not used in I-type)
    "lw"    : ["0000011", "010", None],
    "addi"  : ["0010011", "000", None],
    "sltiu" : ["0010011", "011", None],
    "jalr"  : ["1100111", "000", None],
}
S_type_INSTRUCTIONS={

}
B_type_INSTRUCTIONS={

}
U_type_INSTRUCTIONS={

}
J_type_INSTRUCTIONS={

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
    insbinary.append(inst)


def S_TYPE_INSTRUCTION(instruction):
    print("")
    print("S_TYPE_INSTRUCTION")

def B_TYPE_INSTRUCTION(instruction):
    print("")
    print("B_TYPE_INSTRUCTION")


def U_TYPE_INSTRUCTION(instruction):
    print("")
    print("U_TYPE_INSTRUCTION")


def J_TYPE_INSTRUCTION(instruction):  
    print("")
    print("J_TYPE_INSTRUCTION")




def main():
    x = input("file path ? ")
    try:
        with open(x, "r") as file:
            for line in file:
                line=line.replace("("," ")
                line=line.replace(")"," ")
                instructions.append(line.strip().replace(","," ").split(" "))
        for ins in instructions:
            if ins[0] in R_type_INSTRUCTIONS:
                R_TYPE_INSTRUCTION(ins)
            elif ins[0] in I_type_INSTRUCTIONS:
                I_TYPE_INSTRUCTION(ins)
            elif ins[0] in S_type_INSTRUCTIONS:
                S_TYPE_INSTRUCTION(ins)
            elif ins[0] in B_type_INSTRUCTIONS:
                B_TYPE_INSTRUCTION(ins)
            elif ins[0] in U_type_INSTRUCTIONS:
                U_TYPE_INSTRUCTION(ins)
            elif ins[0] in J_type_INSTRUCTIONS:
                J_TYPE_INSTRUCTION(ins)
        with open("program.txt", "w") as file:
            for inst in insbinary:
                file.write(inst + "\n")
        print("Commands translated to binary in program.txt")
    except:
        print("Syntax Error")
    
main()