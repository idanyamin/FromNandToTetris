// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(initI)
@SCREEN
D=A
@addr
M=D // addr = 16384


@i // init i with 0
M=0

(LOOP)
@i
M=M+1

@8193
D=A
@i
D=D-M // d=8192-i

@initI
D;JEQ


@KBD
D=M

@BLACK
D;JGT

// white coloring
@addr
A=M
M=0 // turn pixels into black
@addr
M=M+1 // ADDR =ADDR + 1

@LOOP
0;JMP



(BLACK)
@addr
A=M
M=-1 // turn pixels into black
@addr
M=M+1 // ADDR =ADDR +32

@LOOP
0;JMP



