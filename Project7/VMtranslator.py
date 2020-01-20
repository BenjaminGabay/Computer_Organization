#@author: Benjamin Gabay

import sys

#math operation dictionary
mathOps = {
    "sub": "-",
    "add": "+",
    "and": "&",
    "or": "|",
    "neg": "-",
    "not": "!"
}

#segPointer dictionary
segPointers = {
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
    "local": "LCL",
    "temp": "5",
    "pointer": "3"
}

#Global gt, lt, eq counters
gtCount = 0
ltCount = 0
eqCount = 0

#Hack constants
POP = "@SP\n"+"AM=M-1\n"+"D=M\n"
GET_M = "@SP\n"+"A=M-1\n"
PUSH = "@SP\n"+"AM=M+1\n"+"A=A-1\n"+"M=D\n"

#Math operation with two arguments
def twoArg(cmd):
    mathOp = mathOps.get(cmd[0], cmd[0] + "not found ")
    assign = "M=M" + mathOp + "D\n"
    return POP + GET_M + assign

#Math operation with one arguments
def oneArg(cmd):
    mathOp = mathOps.get(cmd[0], cmd[0] + "not found ")
    assign = "M=" + mathOp + "M\n"
    return GET_M + assign

#Compare operations
def compare(cmd):
    global gtCount
    global ltCount
    global eqCount
    label = ""
    test = ""

    if cmd[0] == "gt":
        label = "gtTrue" + str(gtCount)
        test = "@" + label + "\nD;JGT\n"
        gtCount += 1
    if cmd[0] == "eq":
        label = "eqTrue" + str(eqCount)
        test = "@" + label + "\nD;JEQ\n"
        eqCount += 1
    if cmd[0] == "lt":
        label = "ltTrue" + str(ltCount)
        test = "@" + label + "\nD;JLT\n"
        ltCount += 1
  
    diffTrue = "D=M-D\n"+"M=-1\n"
    makeFalse = "@SP\n"+"A=M-1\n"+"M=0\n"
    label = "(" + label + ")\n"

    return POP + GET_M + diffTrue + test + makeFalse + label

#Push operation
def push(cmd):
    seg = cmd[1]
    index = cmd[2]

    if seg == "constant":
        value = "@" + index + "\nD=A\n"
    elif seg == "static":
        fileName = sys.argv[1][0 : sys.argv[1].find(".vm")]
        value = "@" + fileName + "." + index + "\nD=M\n"
    else:
        if seg == "temp" or seg == "pointer":
            var = "A"
        else:
            var = "M"
        pointer = segPointers.get(seg, "invalid segment: " + seg + "\n")
        valueIndex = "@" + index + "\nD=A\n"
        valuePointer = "@" + pointer + "\nA=" + var + "+D\nD=M\n"
        value = valueIndex + valuePointer

    return value + PUSH

#Pop operation
def pop(cmd):
    seg = cmd[1]
    index = cmd[2]

    if seg == "static":
        fileName = sys.argv[1][0 : sys.argv[1].find(".vm")]
        pointer = "@" + fileName + "." + index + "\nM=D\n"
        return POP + pointer
  
    if seg == "temp" or seg == "pointer":
        var = "A"
    else:
        var = "M"
    index = "@" + index + "\nD=A\n"
    pointer = segPointers.get(seg, "invalid segment: " + seg + "\n")
    addressR13 = "@" + pointer + "\nD=" + var + "+D\n@R13\nM=D\n"
    change = "@R13\nA=M\nM=D\n"

    return index + addressR13 + POP + change

#Translation dictionary to call proper operation
translations = {
    "add": twoArg,
    "sub": twoArg,
    "or" : twoArg,
    "and": twoArg,
    "neg": oneArg,
    "not": oneArg,
    "eq" : compare,
    "gt" : compare,
    "lt" : compare,
    "push" : push,
    "pop"  : pop
}

#translate command to hack assembly
def translate(line):
    cmd = line.split()
    return translations.get(cmd[0], "\n" + cmd[0] + " not found\n")(cmd)

#Gets rid of comments, and blank lines from .nm file
#Only VM commands remain w/out spaces
def strip(line):
    if line[0] == "\n" or (line[0] == "/" and line[1] == "/"):
        return ""
    else:
        return line[:-1]

#Reads from input file and writes to output file
def main():
    #Ensure .asm command line argument is given
    if(len(sys.argv) != 2):
        sys.exit("usage: VMtranslator.py <vm_File>")

    asmFile = sys.argv[1]
    if(asmFile.find(".vm") == -1):
        sys.exit("Usage Error: Input file must be a .asm file")

    fileName = asmFile[0 : asmFile.find(".vm")]
    inFile = open(asmFile, "r")
    outFile = open(fileName + ".asm", "w")

    commands = []
    for line in inFile:
        stripLine = strip(line)
        if stripLine != "":
            commands.append(stripLine)

    for cmd in commands:
       outFile.write(translate(cmd))

    inFile.close()
    outFile.close()

#Calls main function after all functions are defined
if __name__ == "__main__":
    main()