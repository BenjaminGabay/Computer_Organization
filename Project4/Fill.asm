// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.
//@Author: Benjamin Gabay

//Infinte loop to repeat
(LOOP)
    //Determine if key is pressed and follow proper path
    @KBD
    D = M

    @PRESSED
    D ; JGT

    @RELEASED
    0 ; JMP

//Set color to black = -1 = all 1s binary number
(PRESSED)
    D = -1
    @DRAW
    0 ; JMP

//Set color to white = 0 = all 0s binary number
(RELEASED)
    D = 0

//Set every pixel to value of color by starting at max pixel
//  and counting down
(DRAW)
    @color
    M = D
    
    
    @8191   //Total number of pixel values to change
    D = A
    @counter
    M = D

(NEXT)
    //Set pixel position to pixel counter number plus SCREEN shift
    @pos
    M = D
    @SCREEN
    D = A
    @pos
    M = D+M

    //Color pixel at current position
    @color
    D=M
    @pos
    A=M
    M=D

    //Decrememt counter to move pixel location
    @counter
    M = M-1
    D = M
    
    //Color next pixel
    @NEXT
    D ; JGE

    //Repeat loop to look for keyboard input
    @LOOP
    0 ; JMP