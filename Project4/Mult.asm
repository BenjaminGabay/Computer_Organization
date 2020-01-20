// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Do multiplication of R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
//@Author: Benjamin Gabay

//Set initial value of R2 to 0
@R2
M = 0

//If A = 0 then the product will remain 0; end program
@R0
D = M
@END
D ; JEQ

//If B = 0 then the product will remain 0; end program
@R1
D = M
@END
D ; JEQ

//Repeat COMPARE 4 times to shift the bit 0, 1, 2, and 3 positions
//  to compare to values of 1, 2, 4, and 8
//  Assumes multiplier will be a maximum of 15, otherwise program times out
@4
D = A
@counter
M = D
@COMPARE
0 ; JMP

(COMPARE)
    //Decrement counter
    @counter
    M = M-1
    D = M

    //Left shift value of 1 by counter value
    @temp
    M = 1<D
    D = M

    //Determine if B can be made by this specific power of 2
    //  and add A shifted by power of 2 to sum
    @R1
    D = D&M
    @ADD
    D ; JGT
    @counter
    D = M
    @COMPARE
    D ; JGT
    @END
    D ; JEQ

//ADD A shifted by power of 2
(ADD)
    @counter
    D = M
    @R0
    D = M<D
    @R2
    M = D+M
    @counter
    D = M
    @COMPARE
    D ; JGT

(END)
    @END
    0 ; JMP