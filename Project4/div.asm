// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/div.asm

// Divides R0 by R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
//@Author: Benjamin Gabay

//Load R2 with -1 to start
@R2
M = -1

(SUBTRACT)
    //Increment R2
    @R2
    M = M+1

    //Subtract R1 from R0
    @R1
    D = M
    @R0
    M = M-D
    D = M

    //Repeat while R0 >= 0
    @SUBTRACT
    D ; JGE

(END)
    @END
    0 ; JMP