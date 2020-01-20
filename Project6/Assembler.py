#@author: Benjamin Gabay

import sys

#comp dictionary
comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

#dest dictionary
dest = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

#jump dictionary
jump = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

#Dictionary table of all symbols, labels, and variables
symTable = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576
}
#Add R0-R15 to Symbol Table
for i in range(0, 16):
    symTable["R"+str(i)] = i
#Next location in memory
memLoc = 16

#Dictionary of instructions
instructions = {}

#Normalize c-instructions to have a comp, dest, and jump component
#separated by specific operators
def normalize(instruct):
    if not "=" in instruct:
        instruct = "null=" + instruct
    if not ";" in instruct:
        instruct = instruct + ";null"
    return instruct

#Return the front 13 bits of the translated c-instruction
def c_instruction(instruct):
    instruct = normalize(instruct)
    splitInstruct = instruct.split("=")
    destCode = dest.get(splitInstruct[0], "destFAIL")
    splitInstruct = splitInstruct[1].split(";")
    compCode = comp.get(splitInstruct[0], "compFAIL")
    jumpCode = jump.get(splitInstruct[1], "jumpFAIL")
    return compCode + destCode + jumpCode

#Return 16 bits of 15 bit value of translated a-instruction
def a_instruction(instruct):
    global memLoc
    if instruct[0].isalpha():
        if not instruct in symTable:
            symTable[instruct] = memLoc
            memLoc += 1
        return bin(symTable[instruct])[2:].zfill(16)
    else:
        return bin(int(instruct))[2:].zfill(16)

#Gets rid of comments, blank lines, and spaces from .asm file
#Only labels and instructions remain w/out spaces
def strip(line):
    if line[0] == "\n" or (line[0] == "/" and line[1] == "/"):
        return ""
    elif line[0] == " ":
        return strip(line[1:])
    else:
        return line[0] + strip(line[1:])

#Reads from input file and writes to output file by doing
#Pass 1 and then Pass 2 of the .asm file instructions
def main():
    #Ensure .asm command line argument is given
    if(len(sys.argv) != 2):
        sys.exit("usage: Assembler.py <asmFile>")

    asmFile = sys.argv[1]
    if(asmFile.find(".asm") == -1):
        sys.exit("Usage Error: Input file must be a .asm file")

    fileName = asmFile[0 : asmFile.find(".asm")]
    inFile = open(asmFile, "r")
    outFile = open(fileName + ".hack", "w")

    #Pass 1
    instructNum = 0
    inLines = inFile.readlines()
    for line in inLines:
        stripLine = strip(line)#[:-1]
        if stripLine != "":
            if stripLine[0] == "(" and stripLine[-1] == ")":
                symTable[stripLine[1:-1]] = instructNum
            else:
                instructions[instructNum] = stripLine
                instructNum += 1

    #Pass 2
    for num in range(0, instructNum):
        instruct = instructions[num]
        if instruct[0] == "@":
            outFile.write(a_instruction(instruct[1:]) + "\n")
        else:
            outFile.write("111" + c_instruction(instruct) + "\n")

    inFile.close()
    outFile.close()

#Calls main function after all functions are defined
if __name__ == "__main__":
    main()