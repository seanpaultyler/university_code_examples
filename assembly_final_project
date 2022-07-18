TITLE LLProcedure

; Author: Sean Tyler
; Description: A program incorporating low-level I/O procedures and macros that will
;			   request 10 integers and floats, validate them, and then display them, 
;			   their sum, and their average.


	NUM_INPUTS			= 10
	BUFFER_SIZE			= 500

INCLUDE Irvine32.inc


.data
	; program information
	programInfo			BYTE	"Programming Assignment 6: Designing low-level I/O Procedures",13,10,
								"    Author: Sean Tyler",13,10,13,10,0

	; user prompts / information strings
	promptOverview		BYTE	"First, provide ",0
	promptOverview2		BYTE	" signed integers, then ",0
	promptOverview3		BYTE	" signed decimal numbers.",13,10,
								"(+) is optional; numbers are assumed positive if not signed. ",13,10,
								"Numbers must be between -2,147,483,648 and 2,147,483,647, inclusive.",13,10,13,10,
								"After entering each set of numbers, a list of the numbers, ",13,10,
								"their sum, and their average will be displayed.",13,10,13,10,0
	integerPrompt		BYTE	". Enter a signed integer: ",0
	floatPrompt			BYTE	". Enter a signed decimal: ",0
	runningSumStr		BYTE	"Running Total: ",0
	invalidNumber		BYTE	"That number was invalid; please only use numbers in range with one sign character in front.",13,10,0
	nextSectionStr		BYTE	"The next section will repeat this functionality, but with float values.",13,10,13,10,0
	sectionDivider		BYTE	13,10,"----------------------------------------------------------------------",13,10,13,10,0

	; result strings
	intResultHeader		BYTE	"You entered the following integers: ",13,10,0
	floatResultHeader	BYTE	"You entered the following decimal numbers: ",13,10,0
	sumStr				BYTE	"The sum of these numbers is: ",0
	averageStr			BYTE	"The rounded average is: ",0

	; farewell message
	goodbyeStr			BYTE	"Enjoy your numbers and results!  Have a great day!",13,10,13,10,0

	; EC strings
	EC1Str				BYTE	"**EC - Each input line is numbered and has a running total of valid numbers.",13,10,0
	EC2Str				BYTE	"**EC - Functionality for float values is included.",13,10,13,10,0

	; input buffer and arrays
	buffer				BYTE	BUFFER_SIZE DUP(0)
	intArray			SDWORD	NUM_INPUTS  DUP(?)
	floatArray			REAL4	NUM_INPUTS  DUP(?)

	; var trackers
	runningSum			SDWORD	0
	runningSumF			REAL4	?
	inputCount			SDWORD	NUM_INPUTS

.code

; ---------------------------------------------------------------------------------; 
; Name: mGetString
;
; Prompts and gets a string value from the user.  Also handles
; displaying the running total for EC1.
;
; Preconditions: None.  Registers save
;
; Receives:
;	count = which input is being requested
;	prompt = The text to display to the user before input.
;	runSumStr = the header for the running sum display
;	buffer = the buffer to collected user input into
;	runSumAddr = the running sum of previous user entries.
;	floatBool = bool: treat the numbers as integers (false) or float values (true) 
;
; Returns:
;	buffer = the buffer with collected user input.
;	inputLength = the out var for how many characters the user enters.
; ---------------------------------------------------------------------------------;
mGetString MACRO count, prompt, runSumStr, buffer, inputLength, runSumAddr, floatBool
	LOCAL _float, _cont, _skipRT
	; save registers
	PUSH EAX
	PUSH ECX
	PUSH EDX
	PUSH ESI

	; get running sum.  If first entry, skip printing it.
	MOV  ESI, runSumAddr
	MOV  EAX, [ESI]
	MOV  EDX, count
	CMP  EDX, 1
	JLE _skipRT

	; display sum header.
	MOV  EDX, runSumStr
	CALL WriteString

	; WriteVal (or WriteFloatVal) to display sum.
	PUSH buffer	
	PUSH EAX
	MOV  EDX, floatBool
	CMP  EDX, 1
	JE   _float 
	CALL WriteVal		
	JMP _cont
_float:
	CALL WriteFloatVal
_cont:
	CALL Crlf
	CALL Crlf

_skipRT:
	; display input #
	PUSH buffer	
	PUSH count
	CALL WriteVal

	; display prompt and call for string input.
	MOV  EDX, prompt
	CALL WriteString
	MOV  EDX, buffer
	MOV  ECX, BUFFER_SIZE
	CALL ReadString
	MOV  inputLength, EAX

	; restore regs
	POP ESI
	POP EDX
	POP ECX
	POP EAX

ENDM

; ---------------------------------------------------------------------------------; 
; Name: mDisplayString
;
; Writes a provided string to the display.
;
; Preconditions: None
;
; Postconditions: string written to display.
;
; Receives:
;	stringOffset = the offset of the string to display.
;
; Returns:
;		N/A
; ---------------------------------------------------------------------------------;
mDisplayString MACRO stringOffset
	
	; save reg, display string, restore.
	PUSH EDX
	MOV  EDX, stringOffset
	CALL WriteString
	POP  EDX 

ENDM

main PROC

;------------------------------------------------------------------------------;
;	Introduction to program:  
;		Display program info and introduction.
;------------------------------------------------------------------------------;

	mDisplayString OFFSET programInfo
	mDisplayString OFFSET EC1Str
	mDisplayString OFFSET EC2Str
	mDisplayString OFFSET promptOverview
	
	PUSH OFFSET buffer
	PUSH NUM_INPUTS
	CALL WriteVal

	mDisplayString OFFSET promptOverview2

	PUSH OFFSET buffer
	PUSH NUM_INPUTS
	CALL WriteVal

	mDisplayString OFFSET promptOVerview3
	mDisplayString OFFSET sectionDivider

;------------------------------------------------------------------------------;
; Integer input loop:  
;		Pass arguments and call ReadVal in a loop to get, validate,
;		 and store NUM_INPUTS amount of integers from user.
;------------------------------------------------------------------------------;

	; set counters, ebx tracks valid input count.
	MOV ECX, NUM_INPUTS
	XOR EBX, EBX	
	MOV EDI, OFFSET intArray
_intLoop:
	; inc EBX
	ADD  EBX, 1

	; args for ReadVal	
	PUSH EDI
	PUSH OFFSET runningSum
	PUSH OFFSET runningSumStr	
	PUSH EBX	
	PUSH OFFSET buffer
	PUSH OFFSET integerPrompt
	PUSH OFFSET invalidNumber	
	CALL ReadVal

	; inc EDI to next spot in array and loop.
	ADD EDI, 4
	LOOP _intLoop	
	CALL Crlf
	CALL Crlf

;------------------------------------------------------------------------------;
; Integer display loop; and sum and avg:  
;		Pass arguments and call WriteVal in a loop, which will write out each
;		 stored integer as a string, along with their total sum and average.	
;------------------------------------------------------------------------------;

	mDisplayString OFFSET intResultHeader

	; set counter and pointers.
	MOV ECX, NUM_INPUTS
	MOV ESI, OFFSET intArray

_writeLoop:	
	; fetch number
	LODSD	

	; Call writeVal to convert and print
	PUSH OFFSET buffer		
	PUSH EAX
	CALL WriteVal
	
	; add ', ' after each num, except last.
	CMP ECX, 1
	JLE _skipComma
	MOV  AL, ','
	CALL WriteChar
	MOV  AL, ' '
	CALL WriteChar	

_skipComma:
	LOOP _writeLoop
	CALL Crlf

	; display sum.	
	mDisplayString OFFSET sumStr		
	PUSH OFFSET buffer
	PUSH runningSum
	CALL WriteVal
	CALL Crlf

	; calculate and display average.
	mDisplayString OFFSET averageStr	
	MOV  EAX, runningSum
	MOV  EBX, NUM_INPUTS
	CDQ
	IDIV EBX
	PUSH OFFSET BUFFER
	PUSH EAX
	CALL WriteVal
	CALL Crlf

	; pause and wait for key press to continue.
	mDisplayString OFFSET sectionDivider
	mDisplayString OFFSET nextSectionStr
	CALL WaitMsg
	mDisplayString OFFSET sectionDivider

;------------------------------------------------------------------------------;
; Float input loop:  Pass arguments and call ReadFloatVal in a loop
;		to get, validate, and store NUM_INPUTS amount of floats from user.
;------------------------------------------------------------------------------;

; set counter and pointers.  ebx tracks valid input count.
	MOV ECX, NUM_INPUTS
	XOR EBX, EBX
	MOV EDI, OFFSET floatArray
	MOV runningSumF, 0

_floatLoop:
	; inc EBX to track valid input count.
	ADD  EBX, 1

	; args for ReadFloatVal
	PUSH EDI
	PUSH OFFSET runningSumF
	PUSH OFFSET runningSumStr	
	PUSH EBX	
	PUSH OFFSET buffer
	PUSH OFFSET floatPrompt
	PUSH OFFSET invalidNumber	
	CALL ReadFloatVal

	; inc EDI to next spot in array and loop.
	ADD EDI, 4
	LOOP _floatLoop
	CALL Crlf
	CALL Crlf

;------------------------------------------------------------------------------;
; Float display loop; and sum and average:  
;		Pass arguments and call WriteFloatVal in a loop, which will write out each
;		 stored float as a string, along with their total sum and average.	
;------------------------------------------------------------------------------;

	mDisplayString OFFSET floatResultHeader

	; set counter and pointers.  ebx tracks valid input count.
	XOR EBX, EBX
	MOV ECX, NUM_INPUTS
	MOV ESI, OFFSET floatArray

_writeFloatLoop:	
	; fetch number
	LODSD	

	; Call writeVal to convert and print
	PUSH OFFSET buffer		
	PUSH EAX
	CALL WriteFloatVal
	
	; add ', ' after each num, except last.
	CMP ECX, 1
	JLE _skipFloatComma
	MOV  AL, ','
	CALL WriteChar
	MOV  AL, ' '
	CALL WriteChar	

_skipFloatComma:
	LOOP _writeFloatLoop	
	CALL Crlf
	
	; display sum.
	mDisplayString OFFSET sumStr
	PUSH OFFSET buffer
	PUSH runningSumF
	CALL WriteFloatVal
	CALL Crlf

	; calculate fp avg
	mDisplayString OFFSET averageStr
	FLD runningSumF
	FILD inputCount
	FDIV
	FSTP runningSumF
	
	; display avg
	PUSH OFFSET buffer
	PUSH runningSumF
	CALL WriteFloatVal
	CALL Crlf

;---------------------------------------------------------------------
;	Program Exit:
;		Close the program with a goodbye message.
;---------------------------------------------------------------------

	mDisplayString OFFSET goodbyeStr
	INVOKE ExitProcess, 0

main ENDP

;--------------------------------------------------------------------------------------------------------------------
; Name: ReadVal
;
; Description: Reads a value from user input and translates the received
;		string into a numeric SDWORD, storing the value in a provided array.
;
; Preconditions: invalid number, input prompt, and running sum header strings are set and on stack; buffer address 
;			for string input, integer arrray address for current element, and input count (# in sequence, 
;			e.g. 1. Enter: 2. Enter), on stack.
;
; Postconditions:  No register changes; intArray[element] set to SDWORD converted from input string.
;
; Receives: 
;		[EBP + 8]			= invalidNumber	
;		[EBP + 12]			= integerPrompt	
;		[EBP + 16]			= buffer address
;		[EBP + 20]			= inputCount		
;		[EBP + 24]			= runningSumStr
;		[EBP + 28]			= runningSum
;		[EBP + 32]			= intArray[element]
;
; Returns: intArray[element] as SDWORD from input string.
;--------------------------------------------------------------------------------------------------------------------

ReadVal PROC USES EAX EBX ECX EDX ESI EDI
	LOCAL runningTotal:SDWORD, inputLength:DWORD, negative:BYTE

	; Initialize local vars
	MOV  runningTotal, 0		; used during loop below to track each digits contribution to sum
	MOV  inputLength, 0			; output from macro, how many characters were entered.
	MOV  negative, 0			; determines how a number is treated if the user places a - in front of a string.

_userInput:

	; set ESI at start of buffer
	MOV  ESI, [EBP + 16]	
	CLD

	; get input
	; params:  input count, string, runningTotalStr, buffer(out), inpLen(out), runningTot, float? bool
	mGetString [EBP + 20], [EBP + 12], [EBP + 24], [EBP + 16],   inputLength,  [EBP + 28],      0

	; set ESI to buffer start, EDX to end of input
	MOV  ESI, [EBP + 16]
	MOV  EDX, ESI
	ADD  EDX, inputLength

	_validationLoop:	
		; loop through each byte, validating range
 		CMP ESI, EDX
		JGE _finishValidation

		; load char.  Set EBX to track char position for sign validation.
		XOR  EAX, EAX
		MOV  EBX, ESI 
		LODSB
				
		; check range.  if below, char may be a sign. above ,invalid.
		CMP AL, 48
		JL _checkSign
		CMP AL, 57
		JG _invalid

	_calculateNumber:

		; byte is valid number, add num - 48 to 10 * runningTotal, check for overflow
		SUB  EAX, 48
		MOV  EBX, runningTotal
		IMUL EBX, 10		
		JO _invalid 

		; if negative, subtract digit
		CMP negative, 0
		JE  _continue
		NEG  EAX
	_continue:
		ADD  EBX, EAX
		JO _invalid

		; else save and continue
		MOV  runningTotal, EBX
		JMP _validationLoop

	_checkSign:
		; if not a digit and not in front, invalid.
		CMP EBX, [EBP + 16]
		JG  _invalid
	
		; determine if sign, if -, set negative bool.
		CMP  AL, 43
		JE   _validationLoop
		CMP  AL, 45
		JNE  _invalid
		MOV  negative, 1

		; continue to next number.
		JMP  _validationLoop

_invalid:
		; display error message and prompt reentry
		MOV runningTotal, 0
		mDisplayString [EBP + 8]
		JMP _userInput

;----
;
;
_finishValidation:

	; store in array, and add running total to grand running total.
	MOV EAX, runningTotal
	MOV EDI, [EBP + 32]			; storage array element
	MOV [EDI], EAX
	MOV EBX, [EBP + 28]			; grand running total
	ADD [EBX], EAX		

	; clear buffer after use.
	MOV ECX, inputLength
	MOV EAX, 0
	MOV EDI, [EBP + 16]
	REP STOSB

	RET  28

ReadVal ENDP

;--------------------------------------------------------------------------------------------------------------------
; Name: WriteVal
;
; Description: Converts an SDWORD numeric value to a string and displays it.
;
; Preconditions: SDWORD to convert and display, and temporary buffer address, on stack.
;
; Postconditions:  No register changes; SDWORD displayed as string.
;
; Receives: 
;		[EBP + 28]			= number :SDWORD
;		[EBP + 32]			= buffer address
;
; Returns: N/A
;--------------------------------------------------------------------------------------------------------------------

WriteVal PROC USES EAX EBX ECX EDX EDI EBP

	; set pointer
	MOV EBP, ESP

	; calculate how long the number is
	MOV  ECX, -1
	MOV  EAX, [EBP + 28]
	CMP  EAX, 0
	JGE _continue	; if negative, add space for sign at front.
	ADD  ECX, 1

_continue:
	; repeatedly divide by 10 until 0.
	PUSH EAX
	MOV  EBX, 10
_digitCount:
	ADD  ECX, 1
	CDQ
	IDIV EBX
	CMP  EAX, 0
	JNE _digitCount

	; set write pointer to buffer + # of digits, then set dir flag and start will null char
	MOV  EDI,  [EBP + 32]
	ADD  EDI, ECX
	ADD  EDI, 1
	STD
	MOV AL, 0
	STOSB

	; divide by 10, get remainder.
	POP EAX
_conversionLoop:
	CDQ
	IDIV EBX		; EDX = 10
	CMP  EDX, 0		; if negative, negate for positive
	JGE  _notNeg
	NEG  EDX

_notNeg:
	ADD  EDX, 48	; r + 48 is ascii char.
	PUSH EAX		; store remaining dividend, write remainder to buffer.	
	MOV  AL, DL
	STOSB	

	; restore dividend, if 0, end write.
	POP  EAX
	CMP  EAX, 0
	JNE  _conversionLoop

	; add neg sign if needed then call write macro.
_writeString:
	MOV  EAX, [EBP + 28]
	CMP  EAX, 0
	JGE _skipNeg
	MOV AL, '-'
	STOSB
_skipNeg:
	mDisplayString [EBP + 32]

	; clear buffer after use.
	MOV ECX, EBX
	MOV EAX, 0
	MOV EDI, [EBP + 32]
	REP STOSB

	RET 8

WriteVal ENDP

;--------------------------------------------------------------------------------------------------------------------
; Name: ReadFloatVal
;
; Description: Reads a decimal value from user input and translates the received
;		string into a numeric SDWORD, storing the value in a provided array.
;
; Preconditions: invalid number, input prompt, and running sum header strings are set and on stack; buffer address 
;			for string input, integer arrray address for current element, and input count (# in sequence, 
;			e.g. 1. Enter: 2. Enter), on stack.
;
; Postconditions:  No register changes; intArray[element] set to SDWORD converted from input string.
;
; Receives: 
;		[EBP + 8]			= invalidNumber
;		[EBP + 12]			= floatPrompt
;		[EBP + 16]			= buffer address
;		[EBP + 20]			= inputCount
;		[EBP + 24]			= runningSumStr
;		[EBP + 28]			= runningSumF
;		[EBP + 32]			= intArray[element]
;
; Returns: intArray[element] as SDWORD from input string.
;--------------------------------------------------------------------------------------------------------------------
ReadFloatVal PROC USES EAX EBX ECX EDX ESI EDI
	LOCAL tenDivisor:SDWORD, runningTotal:SDWORD, inputLength:DWORD, negative:BYTE, radix:DWORD

	MOV  tenDivisor, 10
	MOV  runningTotal, 0
	MOV  inputLength, 0
	MOV  negative, 0
	MOV  radix, -1

_userInput:

	; set ESI at start of buffer
	MOV  ESI, [EBP + 16]	
	CLD

	; get input
	; params:  input count,  string,    rsumString, buffer(out),  in len(out), rngSum, float?bool(true)
	mGetString [EBP + 20], [EBP + 12], [EBP + 24], [EBP + 16], inputLength, [EBP + 28], 1

	; quick string oversize check, > 11 is fail, too big for signed # in 32-bit register.
	CMP inputLength, 11
	JG _invalid
	CMP inputLength, 0
	JE _invalid

	; set ESI to buffer start, EDX to end of input
	MOV  ESI, [EBP + 16]
	MOV  EDX, ESI
	ADD  EDX, inputLength

	_validationLoop:	
		; loop through each byte, validating range
 		CMP ESI, EDX
		JGE _finishValidation

		; load char.  Set EBX to track char position for sign validation.
		XOR  EAX, EAX
		MOV  EBX, ESI 
		LODSB
				
		; check range.  if below, char may be a sign or radix. above ,invalid.
		CMP AL, 48
		JL _checkSign
		CMP AL, 57
		JG _invalid

		; byte is valid number, add num - 48 to 10 * runningTotal
		SUB  EAX, 48
		MOV  EBX, runningTotal
		IMUL EBX, 10		
		ADD  EBX, EAX

		; check for overflow
		JO _invalid

		; else save and continue
		MOV  runningTotal, EBX
		JMP _validationLoop

	_checkSign:
		; if radix, mark it.  If radix already set, invalid.
		CMP  AL, 46
		JE	 _checkRadix

		; anything else, if not a digit and not in front, invalid.
		CMP EBX, [EBP + 16]
		JG  _invalid
	
		; determine if sign, if -, set negative bool.		
		CMP  AL, 43
		JE   _validationLoop
		CMP  AL, 45
		JNE  _invalid
		MOV  negative, 1

		; continue to next number.
		JMP  _validationLoop

	_checkRadix:
		CMP radix, -1
		JNE _invalid
		MOV radix, EDX
		SUB radix, ESI		; set to # digits after radix.
		JMP _validationLoop

_invalid:
		; display error message and prompt reentry
		MOV runningTotal, 0
		MOV radix, -1
		mDisplayString [EBP + 8]
		JMP _userInput

_finishValidation:
	; divide by 10x(number of digits after radix), or skip if no radix.
	FILD runningTotal
	CMP radix, -1
	JE  _skipDiv

	MOV ECX, radix
_divLoop:
	FILD tenDivisor
	FDIV
	LOOP _divLoop

_skipDiv:
	; if string had '-' sign, negate.	
	CMP  negative, 0
	JE   _continue
	FCHS
_continue:
	; store in array	
	MOV  EDI, [EBP + 32]
	FST  REAL4 PTR [EDI]

	; add to running float total
	MOV  EBX, [EBP + 28]
	FLD  REAL4 PTR [EBX]
	FADD
	FSTP REAL4 PTR [EBX]

	; clear buffer after use.
	MOV ECX, inputLength
	MOV EAX, 0
	MOV EDI, [EBP + 16]
	REP STOSB

	RET  28

ReadFloatVal ENDP

;--------------------------------------------------------------------------------------------------------------------
; Name: WriteFloatVal
;
; Description: Converts an SDWORD numeric decimal value to a string and displays it.
;
; Preconditions: SDWORD to convert and display, and temporary buffer address, on stack.
;
; Postconditions:  No register changes; SDWORD displayed as string.
;
; Receives: 
;		[EBP + 28]			= number
;		[EBP + 32]			= buffer address
;
; Returns: N/A
;--------------------------------------------------------------------------------------------------------------------
WriteFloatVal PROC USES EAX EBX ECX EDX EDI EBP
	LOCAL intMult:WORD, tempInt:SDWORD, radix:WORD

	; initialize local vars
	MOV  intMult, 100
	MOV  tempInt, 0
	MOV  radix, 0

	; multiply float by 100 and round to get two decimals.
	FLD REAL4 PTR [EBP + 8]
	FILD intMult
	FMUL 
	FISTP tempInt

	; calculate how long the number is
	MOV  ECX, 0
	MOV  EAX, tempInt
	CMP  EAX, 0
	JGE _continue
	NEG  EAX
	ADD  ECX, 1		; ECX + 1 for sign

_continue:
	; repeatedly divide by 10 until 0.
	PUSH EAX
	MOV  EBX, 10
_digitCount:
	ADD  ECX, 1
	CDQ
	IDIV EBX
	CMP  EAX, 0
	JG _digitCount

	; set write pointer to buffer + # of digits, then set dir flag.
	MOV  EDI,  [EBP + 12]
	ADD  EDI, ECX
	STD

	
	; divide by 10, get remainder; r + 48 is ascii char. dec ecx, when ecx=0, add radix
	POP EAX
	MOV ECX, 3
_conversionLoop:	
	SUB ECX, 1
	JNE  _noRadix
	PUSH EAX
	MOV  AL, '.'
	STOSB
	POP  EAX
	JMP _conversionLoop

_noRadix:
	CDQ
	IDIV EBX		; EBX still 10
	ADD  EDX, 48
	
	PUSH EAX		; store remaining dividend, write remainder to buffer.	
	MOV  AL, DL
	STOSB	

	; restore dividend, if 0, end write.
	POP  EAX
	CMP  ECX, 0
	JG	_conversionLoop
	CMP  EAX, 0
	JG  _conversionLoop
	JMP _writeString

	; add radix


	; add neg sign if needed then call write macro.
_writeString:
	MOV  EAX, [EBP + 8]
	CMP  EAX, 0
	JGE _skipNeg
	MOV AL, '-'
	STOSB
_skipNeg:
	mDisplayString [EBP + 12]

	; clear buffer after use.
	MOV ECX, EBX
	MOV EAX, 0
	MOV EDI, [EBP + 12]
	REP STOSB

	RET 8

WriteFloatVal ENDP

END main
