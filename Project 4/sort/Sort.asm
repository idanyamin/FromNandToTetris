// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// sort an array of integers R14 contains the address
// and R15 constains the length

// Put your code here.

// ------------ sort ---------------//
@counterOut
M=0

// ------ loop outer --------
(loopOuter)

// init counterInner
@counterInner
M=0

	// ------ loop Inner --------
	(loopInner)
	// put arr[counterInner] in B
	@R14
	D=M

	@counterInner
	D=D+M

	A=D
	D=M

	@B
	M=D

	// put arr[counterInner + 1] in C
	@R14
	D=M

	@counterInner
	D=D+M
	D=D+1
	A=D
	D=M

	@C
	M=D

	// if c-b>0 jump to swap

	@C
	D=M

	@B
	D=D-M

	@SWAP
	D;JGT

	(returnFromSwap)
	// load b and c to arr[inner] and arr[inner+1]

	@R14
	D=M

	@counterInner
	D=D+M

	@ADDRESS
	M=D

	@B
	D=M

	@ADDRESS
	A=M
	M=D

	@R14
	D=M

	@counterInner
	D=D+M

	@ADDRESS
	M=D+1

	@C
	D=M

	@ADDRESS
	A=M
	M=D
	


	@R15
	D=M

	@counterInner
	M=M+1
	D=D-M
	D=D-1

	@loopInner
	D;JGT

@R15
D=M

@counterOut
M=M+1
D=D-M

@loopOuter
D;JGT

(FINISH)
@FINISH
0;JMP







//---------swap--------------
// put in a the first number put in b the second number
(SWAP)
// put a in temp
@B
D=M

@TEMP
M=D

// put C in B
@C
D=M

@B
M=D

// put temp in C
@TEMP
D=M

@C
M=D

@returnFromSwap
0;JMP

//--------- end swap--------------



