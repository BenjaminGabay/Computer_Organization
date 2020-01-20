//This asm computes the modulo of two numbers
//Assuming R0 stores the number a and R1 stores the number b (b can not be 0)
//so in normal programming language, the goal is to compute RAM[R0]%RAM[R1]
//The result will be put to RAM[R2]
//Assuming RAM[R1] is positive integer and RAM[R0] is non-negative integer
//write your code here.
//@Author: Benjamin Gabay

//Set R2 to A and end if A is 0
@R0
D = M
@R2
M = D
@END
D ; JEQ

//Subtract B from A until A is negative
(SUBTRACT)
    @R1
    D = M
    @R2
    M = M-D
    D = M
    @ADD_MOD
    D ; JLT
    @SUBTRACT
    0 ; JMP

//Add B back to A to find remainder
(ADD_MOD)
    @R1
    D = M
    @R2
    M = D+M

(END)
    @END
    0 ; JMP