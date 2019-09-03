// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// init counter with R0
@R0
D=M
@POS_COUNTER
D;JGE
@COUNTER
M=D
D=0
M=D-M
@INIT_SUM
0;JMP

(POS_COUNTER)
@COUNTER
M=D

(INIT_SUM)
// init sum to 0
@R2
M=0

@COUNTER
D=M

// if counter is zero than finish the program
@FINISH
D;JEQ

@loopPos
D;JGT

// *loop negative*

(loopNeg)
// put R1 in the register d
@R1
D=M

// update sum
@R2
M=M+D

// update counter
@COUNTER
M=M+1

@COUNTER
D=M

// if counter greater than 0 jump to loop
@loopNeg
D;JGT

@FINISH
0;JMP
// *endloop*


// *loop positive*
(loopPos)

// put R1 in the register d
@R1
D=M

// update sum
@R2
M=M+D

// update counter
@COUNTER
M=M-1

@COUNTER
D=M

// if counter greater than 0 jump to loop
@loopPos
D;JGT

// *endloop*
// fix the sign of the result
@R0
D=M
@FIX_RES
D;JLT
@FINISH
0;JMP

(FIX_RES) // IF R0 < 0 THE RESULT MUST BE RES*(-1)
@R2
D=0
M=D-M

// infinite loop
(FINISH)
@FINISH
0;JMP
