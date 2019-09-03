// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Divide.asm

// Divides R13 aby R14 and stores the result in R15.
// (R13, R14, R15 refer to RAM[13], RAM[14], and RAM[15], respectively.)

// Put your code here.

//init result to 0


// INIT VARIABLES
@R15
M=0

@0
D=A

@POS
M=D-1

@R14 // jump to 14_POS if ram[14] is positive or zero
D=M
@14_POS
D;JGT

@14_ZERO // if zero end program
D;JEQ

//negative
@DIVISOR // make divisor positive
M=D
D=0
M=D-M

@INIT_DIVIDEND
0;JMP

(14_ZERO)
@FINISH
0;JMP

(14_POS)
@DIVISOR
M=D

@INIT_DIVIDEND
0;JMP

(INIT_DIVIDEND) // if r13 is positive jump to 13_pos
@R13
D=M
@13_POS
D;JGE

//r13 is negative
@DIVIDEND // make dividend negative
M=D
D=0
M=D-M

@END_INIT // start program
0;JMP

(13_POS)
@DIVIDEND
M=D


(END_INIT)


(LOOP)

	@DIVIDEND
	D=M

	@DIVISOR
	D=D-M

	// jump to endLoop if dividend <= divisor

	@endLoop
	D;JLT

	@DIVISOR
	M=M<<

	@POS
	M=M+1

	@LOOP
	0;JMP

(endLoop)

@DIVISOR
M=M>>

(LOOP2)

	@POS
	D=M+1

	//if pos+1 <= 0 jump to endLoop2

	@endLoop2
	D;JLE

	@DIVIDEND
	D=M

	@DIVISOR
	D=D-M
	
	//if dividend - divisor >= 0 jump to IF

	@IF
	D;JGE

	(endIf)

	@DIVISOR
	M=M>>

	@POS
	M=M-1

	@LOOP2
	0;JMP

(endLoop2)


@FIX_RES
0;JMP


// if dividend >= divisor

(IF)

	@POS
	D=M

	@COUNTER
	M=D

	@1
	D=A

	@shiftOne
	M=D

	(loopShift)

		@COUNTER
		D=M

		//end loopShift if counter == 0
 
		@endLoopShift
		D;JEQ

		@shiftOne
		M=M<<

		@COUNTER
		M=M-1

		@loopShift
		0;JMP

	(endLoopShift)

	@shiftOne
	D=M

	@R15
	M=M+D

	@DIVISOR
	D=M

	@DIVIDEND
	M=M-D

	@endIf
	0;JMP

(FIX_RES) // decide what is the sign
@R14
D=M
@R14_IS_POS // jump greater than
D;JGT
// R14 IS NEGATIVE

@R13
D=M
@FINISH
D;JLT

// R14 IS NEGATIVE R13 IS POSITIVE
(NEG_RES)
@R15
D=M
M=0
M=M-D
@FINISH
0;JMP

(R14_IS_POS)
@R13
D=M
@FINISH
D;JGE

// R14 IS POSITIVE AND R13 IS NEGATIVE
@NEG_RES
0;JMP

(FINISH)
@FINISH
0;JMP

