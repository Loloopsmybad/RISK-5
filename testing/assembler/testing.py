import os



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

'''
note the ADRESSES ARE AS FFOLOWS

| Address                   | Register | ABI Name | Description                          | Saver  |
| 0000_0                    | x0       | zero     | Hard-wired zero                      | —      |
| 0000_1                    | x1       | ra       | Return address                       | Caller |
| 0001_0                    | x2       | sp       | Stack Pointer                        | Callee |
| 0001_1                    | x3       | gp       | Global Pointer                       | —      |
| 0010_0                    | x4       | tp       | Thread Pointer                       | —      |
| 0010_1                    | x5       | t0       | Temporary / alternate link register  | Caller |
| 00_{110,111}              | x6–7     | t1–2     | Temporaries                          | Caller |
| 0100_0                    | x8       | s0/fp    | Saved register / frame pointer       | Callee |
| 0100_1                    | x9       | s1       | Saved register                       | Callee |
| 0101_{0,1}                | x10–11   | a0–1     | Function arguments / return values   | Caller |
| (011_{00-11}),(1000_{0,1})| x12–17   | a2–7     | Function arguments        | Caller |
| 1_{0010-1011}             | x18–27   | s2–11    | Saved registers                      | Caller |
| 111_{00-11}               | x28–31   | t3–6     | Temporaries                          | Caller |
+-------------------+----------+----------+--------------------------------------+--------+

'''
def R_TYPE_INSTRUCTION():
    print("R_TYPE_INSTRUCTION")
    '''
    Fields: funct7 | rs2 | rs1 | funct3 | rd | opcode

    Example: add s1, s2, s3
    meaning: s1 = s2 + s3

    funct7  = identifies ADD operation
    rs2     = s3 (second source register)
    rs1     = s2 (first source register)  
    funct3  = helps identify ADD
    rd      = s1 (where result goes)
    opcode  = identifies R-type
    '''




def I_TYPE_INSTRUCTION():
    print("I_TYPE_INSTRUCTION")

def S_TYPE_INSTRUCTION():
    print("S_TYPE_INSTRUCTION")

def B_TYPE_INSTRUCTION():
    print("B_TYPE_INSTRUCTION")


def U_TYPE_INSTRUCTION():
    print("U_TYPE_INSTRUCTION")


def J_TYPE_INSTRUCTION():  
    print("J_TYPE_INSTRUCTION")




def main():
    x = input("file path ? ")
    try:
    with open(x, 'r') as file:
        content = file.read()
        print(content)
    except FileNotFoundError:
        print("File not found.")