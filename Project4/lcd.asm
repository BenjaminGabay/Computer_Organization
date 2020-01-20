//Using Euclidean algorithm to find the larget common divisor of two non-negative integers
//Assuming RAM[R0] stores the first integer and RAM[R1] stores the second integer
//RAM[R2] stores the result
//Write your code here
//@Author: Benjamin Gabay

//Set initial values of A and B
@R0
D = M
@A
M = D
@R1
D = M
@B
M = D

//Find GCD of A and B
(GCD)
    //If A=0, GCD=B
    @A
    D = M
    @USE_B
    D ; JEQ
    //If B=0, GCD=A
    @B
    D = M
    @USE_A
    D ; JEQ
    
    //R=A
    @A
    D = M
    @R
    M = D

    //Find R, remainder of A/B
    (FIND_R_1)
        @B
        D = M
        @R
        M = M-D
        D = M
        @FIND_R_2
        D ; JLT
        @FIND_R_1
        0 ; JMP

    //Set R
    //A=B
    //B=R
    //Find GCD again of essentially GCD(B, R)
    (FIND_R_2)
        @B
        D = M
        @A
        M = D
        @R
        M = D+M
        D = M
        @B
        M = D
        @GCD
        0 ; JMP

//Set R2 to A
(USE_A)
@A
D = M
@R2
M = D
@END
0 ; JMP

//Set R2 to B
(USE_B)
@B
D = M
@R2
M = D

(END)
    @END
    0 ; JMP