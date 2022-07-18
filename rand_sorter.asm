TITLE Random Number Generator, Sorter, Counter

; Author: Sean Tyler
; Description:  A program that generates and sorts an array of random numbers,
;				calculates the median number and occurrences of each number, and displays
;				the results of each step.

INCLUDE Irvine32.inc

LO			=		10		; lower and
HI			=		29		; upper bound of 
ARRAYSIZE	=		200		; random numbers generated

.data
	; Program title and author.
	titleString		BYTE	"Random Integer Generator, Sorter, and Counter - by Sean Tyler",13,10,13,10,0

	; EC strings.
	ec1Message		BYTE	"**EC1 - Arrays are displayed by column.",13,10,0
	ec2Message		BYTE	"**EC2 - Numbers are generated to a file, then read into the array.",13,10,13,10,0

	; Strings for user information.
	intro1			BYTE	"This program generates ",0
	intro2			BYTE	" random numbers in the range [",0
	intro3			BYTE	"], displays the",13,10,
							"original list, sorts it, calculates and displays the median value, displays",13,10,
							"the list sorted in ascending order, then counts and displays the number of",13,10,
							"instances of each generated value, starting with ",0
	goodbyeStr		BYTE	"Hope you enjoyed your random numbers.  Goodbye!",13,10,13,10,0

	; Display headers.
	unsortedHeader	BYTE	"Your unsorted random numbers:",13,10,0
	medianHeader	BYTE	"The median value of the array: ",0
	sortedHeader	BYTE	"Your sorted random numbers:",13,10,0
	instancesHeader	BYTE	"Your list of instances of each generated number:",13,10,0

	; Random number and count arrays.
	randArray		DWORD	ARRAYSIZE DUP(?)
	counts			DWORD	(HI-LO+1) DUP(?)

	; File info for writing and reading
	fileName		BYTE	"randArray",0
	buffer			DWORD	ARRAYSIZE DUP(?)

.code
main PROC	

	; randomize random generator
	CALL Randomize

	; introduction to display program information.
	PUSH HI
	PUSH LO
	PUSH ARRAYSIZE
	PUSH OFFSET titleString
	PUSH OFFSET ec1Message
	PUSH OFFSET ec2Message
	PUSH OFFSET intro1
	PUSH OFFSET intro2
	PUSH OFFSET intro3
	CALL introduction

	; fillArray to fill array with random values.		
	PUSH OFFSET fileName
	PUSH OFFSET buffer
	PUSH OFFSET randArray	
	PUSH HI
	PUSH LO
	PUSH ARRAYSIZE
	CALL fillArray

	; displayList to display newly filled array.
	PUSH OFFSET unsortedHeader
	PUSH OFFSET randArray
	PUSH ARRAYSIZE
	CALL displayList

	; sortList to sort the array in ascending order.	
	PUSH OFFSET randArray
	PUSH ARRAYSIZE
	CALL sortList

	; displayMedian to show the median value of the array.
	PUSH OFFSET medianHeader
	PUSH OFFSET randArray
	PUSH ARRAYSIZE
	CALL displayMedian

	; displayList to display newly sorted array.
	PUSH OFFSET sortedHeader
	PUSH OFFSET randArray
	PUSH ARRAYSIZE
	CALL displayList

	; countList to count the amount of each number in the array.
	PUSH OFFSET randArray
	PUSH ARRAYSIZE
	PUSH OFFSET counts
	PUSH HI
	PUSH LO
	CALL countList

	; displayList again, with counts info.
	PUSH OFFSET instancesHeader
	PUSH OFFSET counts
	PUSH (HI - LO + 1)
	CALL displayList

	; displayMessage to display goodbye string.
	PUSH OFFSET goodbyeStr
	CALL displayMessage

	Invoke ExitProcess,0	; exit to operating system

main ENDP

;-------------------------------------------------------------------------------------------------------------------
; Name: introduction
;
; Description:  Describes program title, author, functionality, and any other info.
; 
; Preconditions: Six intro strings set, HI, LO, and array size are ints.
;
; Postconditions: Intro strings and info written.  No register change.
;
; Receives: 
;		[EBP + 48]					= HI int
;		[EBP + 44]					= LO int
;		[EBP + 40]					= array size int
;		[EBP + 16,20,24,28,32,36]	= information string addresses 1-6
;
; Returns: N/A
;-------------------------------------------------------------------------------------------------------------------

introduction PROC USES EAX EDX EBP
	
	; set base pointer
	MOV  EBP, ESP

	; title and EC strings
	MOV  EDX, [EBP + 36]
	CALL WriteString
	MOV  EDX, [EBP + 32]
	CALL WriteString
	MOV  EDX, [EBP + 28]
	CALL WriteString

	; intro1
	MOV  EDX, [EBP + 24]
	CALL WriteString

	; print ARRAYSIZE	
	MOV  EAX, [EBP + 40]
	CALL WriteDec
	
	; intro2
	MOV  EDX, [EBP + 20]
	CALL WriteString

	; print 'LO,HI'
	MOV  EAX, [EBP + 44]
	CALL WriteDec
	MOV  AL, ','
	CALL WriteChar
	MOV  EAX, [EBP + 48]
	CALL WriteDec

	; intro3
	MOV  EDX, [EBP + 16]
	CALL WriteString

	; end with LO, '.'
	MOV  EAX, [EBP + 44]
	CALL WriteDec
	MOV  AL, '.'
	CALL WriteChar
	CALL Crlf
	CALL Crlf

	RET  24

introduction ENDP

;-----------------------------------------------------------------------------------------------------------------------------
; Name: fillArray
; 
; Description: Fills an array with random values.
;
; Preconditions: Filename string set and valid, buffer is type DWORD, array is type DWORD, max, min, 
;		and array size are positive ints.
;
; Postconditions: Array is filled with random values; file generated in program directory with array values. 
;				  No register change.
;
; Receives: 
;		[EBP + 48]		= filename string address
;		[EBP + 44]		= buffer address
;		[EBP + 40]		= array address
;		[EBP + 36]		= max int
;		[EBP + 32]		= min int
;		[EBP + 28]		= array size int
;
; Returns: Array at reference address filled with random values.
;-----------------------------------------------------------------------------------------------------------------------------

fillArray PROC USES EAX EBX ECX EDI ESI EBP

	; set base pointer
	MOV  EBP, ESP

	; Create output file
	MOV  EDX, [EBP + 48]		; filename
	CALL CreateOutputFile
	MOV  EBX, EAX

	MOV  ECX, [EBP + 28]		; amount of #s to generate.
	MOV  EDX, [EBP + 44]		; buffer start.

_fillFileLoop:
	; for range [LO, HI], HI + 1 - LO, RandomRange, + LO
	MOV  EAX, [EBP + 36]
	ADD  EAX, 1
	SUB  EAX, [EBP + 32]
	CALL RandomRange
	ADD  EAX, [EBP + 32]

	; write number to buffer, advance EDX to next element.
	MOV  [EDX], EAX
	ADD  EDX, 4
	LOOP _fillFileLoop

	; set EAX to file, EDX to buffer address.
	MOV  EAX, EBX
	MOV  EDX, [EBP + 44]
	MOV  ECX, [EBP + 28]		; arraysize
	IMUL ECX, 4
	CALL WriteToFile

	; Open file.
	MOV  EAX, [EBP + 48]		; filename, openinputfile sets EAX as filehandle for readfromfile.
	CALL OpenInputFile

	; Read from file.
	MOV  EDX, [EBP + 44]		; buffer address
	MOV  ECX, [EBP + 28]		; arraysize
	IMUL ECX, 4
	CALL ReadFromFile
	CALL CloseFile

	; set read/write references.
	MOV  ESI, [EBP + 44]		; buffer
	MOV  EDI, [EBP + 40]		; array
	MOV  ECX, [EBP + 28]		; arraysize

_fillArrayLoop:
	; write to array, advance to next element and repeat for ECX > 0.
	MOV  EAX, [ESI]
	MOV  [EDI], EAX
	ADD  EDI, 4
	ADD  ESI, 4
	LOOP _fillArrayLoop

	RET 24

fillArray ENDP

;-----------------------------------------------------------------------------------------------------------------------------
; Name: sortList
;
; Description:  Sorts a provided array by non-descending order.
; 
; Preconditions:  Array is type DWORD, array size is positive int.
;
; Postconditions: Array is sorted by ascending.  No register change.
;
; Receives:
;		[EBP + 32]		= array address
;		[EBP + 28]		= array size int
;
; Returns: Sorted array at array address.
;-----------------------------------------------------------------------------------------------------------------------------

sortList PROC USES EAX EBX ECX EDX ESI EBP

	; set base pointer
	MOV  EBP, ESP

	; set up registers for insertion sort.
	MOV  EBX, [EBP + 32]

	MOV  ECX, [EBP + 28]
	IMUL ECX, 4
	ADD  ECX, EBX

	ADD  EBX, 4
	MOV  ESI, EBX
	
_indexLoop:						
	_comparisonLoop:
		; while index - 1 >= array start
		MOV  EAX, ESI			
		SUB  EAX, 4
		CMP  EAX, [EBP + 32]	
		JL   _endComparison

		; compare order
		SUB  ESI, 4
		MOV  EDX, [ESI]		
		ADD  ESI, 4
		CMP  EDX, [ESI]	 
		JLE  _endComparison

		; if descending, call exchangeElements to swap elements.
		PUSH ESI
		SUB  ESI, 4
		PUSH ESI
		CALL exchangeElements

		; continue comparing and swapping until non-descending.
		JMP _comparisonLoop

	; for i in range(arrayLength) (EBX < ECX)
_endComparison:  
	ADD  EBX, 4
	MOV  ESI, EBX
	CMP  EBX, ECX
	JL   _indexLoop

	RET	 8

sortList ENDP

;-----------------------------------------------------------------------------------------------------------------------------
; Name: exchangeElements
; 
; Preconditions: Element1 and element2 are same size.
;
; Postconditions: Element1 and element2 swapped.  No register change.
;
; Receives: 
;		[EBP + 24]		= element1 address
;		[EBP + 20]		= element2 address
;
; Returns: Element1 at element2 address, element2 at element1 address.
;
;-----------------------------------------------------------------------------------------------------------------------------

exchangeElements PROC USES EAX ESI EDI EBP

	; set base pointer
	MOV  EBP, ESP

	; exchange elements
	MOV  ESI, [EBP + 24]
	MOV  EDI, [EBP + 20]
	MOV  EAX, [EDI]				; pick up B from index2.
	XCHG EAX, [ESI]				; swap A and B; B is now in index1.
	MOV  [EDI], EAX				; set down A in index2.

	RET  8

exchangeElements ENDP

;-----------------------------------------------------------------------------------------------------------------------------
; Name: displayMedian
;
; Description:  Displays the median of the array of numbers.  If even, displays the average of the middle two numbers,
;		with half up rounding.
; 
; Preconditions: Header string set, array is type DWORD, array size is positive int.
;
; Postconditions: Header and median written.  No register change.
;
; Receives: 
;		[EBP + 28]		= header address
;		[EBP + 24]		= array address
;		[EBP + 20]		= array size int
;
; Returns: N/A
;-----------------------------------------------------------------------------------------------------------------------------

displayMedian PROC USES EAX EBX EDX EBP
	
	; Set base pointer
	MOV  EBP, ESP

	; write header
	MOV  EDX, [EBP + 28]
	CALL WriteString

	; Median is different for even/odd
	MOV  EAX, [EBP + 20]		; array size
	SUB  EAX, 1
	MOV  EBX, 2
	CDQ
	IDIV EBX
	CMP  EDX, 0

	; EAX is middle element in odd arrays, and first middle element in even arrays.
	; x4, add array address to set EAX to proper element.
	IMUL EAX, 4
	ADD  EAX, [EBP + 24]		; array address
	MOV  EDX, EAX				; EDX is set to EAX to retrieve next element if even.
	MOV  EAX, [EAX]
	JNE _even
	JMP _writeNumber

	; even: [EAX + (EAX + 4)] / 2
_even:
	ADD  EDX, 4
	MOV  EDX, [EDX]
	ADD  EAX, EDX
	IMUL EAX, 10				; x10 numerator and divisor to capture fractional remainder as integer.
	IMUL EBX, 10			
	CDQ
	IDIV EBX
	CMP  EDX, 5					; if remainder is greater than 5, round up.
	JL  _writeNumber
	ADD  EAX, 1

_writeNumber:
	CALL WriteDec
	CALL Crlf
	CALL Crlf

	RET  8

displayMedian ENDP

;-----------------------------------------------------------------------------------------------------------------------------
; Name: displayList
; 
; Description: Displays the provided array, 20 elements to a line.
;
; Preconditions: Header string set, array is type DWORD, array size is positive int.
;
; Postconditions: Array contents written by column.  No register change.
;
; Receives: 
;		[EBP + 40]		= header address
;		[EBP + 36]		= array address
;		[EBP + 32]		= array size int
;
; Returns: N/A
;-----------------------------------------------------------------------------------------------------------------------------

displayList PROC USES EAX EBX ECX EDX ESI EDI EBP

	; set base pointer
	MOV  EBP, ESP

	; display header	
	MOV  EDX, [EBP + 40]		; header address
	CALL WriteString

	MOV  ESI, [EBP + 36]		; ESI is now start of array.
	MOV  ECX, [EBP + 32]		; ECX is now number of elements.

	; Calculate number of rows with 20 elements to a row and then the distance between elements in a row. (rows x element size)
	MOV  EAX, ECX
	MOV  EBX, 20
	CDQ
	IDIV EBX
	IMUL EAX, 4
	MOV  EBX, EAX				; EBX is now the offset between elements.
	MOV  EAX, EDX				; EAX is the number of columns with addlt. 4 added to offset between elements.
	PUSH EAX
	XOR  EDX, EDX				; EDX will track elements to line wrap at 20.
	MOV  EDI, ESI				; EDI is now ESI, to mark start and increment by 4 each line wrap.

_displayLoop:		

	PUSH EAX					; save remainder to free EAX.

_writeNumber:
	MOV  AL, ' '
	CALL WriteChar
	MOV  EAX, [ESI]				; write number
	CALL WriteDec
	POP  EAX					; restore remainder.

	; add offset, and if remainder, add addtl. 4
	ADD  ESI, EBX	
	CMP  EAX, 0
	JE	 _noRemainder
	SUB  EAX, 1
	ADD  ESI, 4
_noRemainder:
	ADD  EDX, 1
	CMP  EDX, 20
	JGE  _wrapLine	
	JMP  _toLoop

	; advance to next line, increment EDI, and set pointers and counters
_wrapLine:
	CALL Crlf
	ADD  EDI, 4
	MOV  ESI, EDI			
	XOR  EDX, EDX
	MOV  EAX, [ESP]				; reset remainder.

_toLoop:
	LOOP _displayLoop
	POP  EAX

	CALL Crlf
	CALL Crlf

	RET  12

displayList ENDP


;-----------------------------------------------------------------------------------------------------------------------------
; Name: countList
;
; Description: Counts and fills an array of occurrences of each number in a provided array.
; 
; Preconditions: Min, max, and arraysize ints are positive, arrays are type DWORD.
;
; Postconditions: array2 will hold counts of occurrences of numbers in array1.  No register change.
;
; Receives: 
;		[EBP + 48]		= array1 address
;		[EBP + 44]		= array1 int size
;		[EBP + 40]		= array2 address
;		[EBP + 36]		= max int in range
;		[EBP + 32]		= min int in range
;
; Returns: Array of occurrences of numbers in array1 at array2 address.
;-----------------------------------------------------------------------------------------------------------------------------
countList PROC USES EAX EBX ECX EDX ESI EDI EBP

	; set base pointer
	MOV  EBP, ESP

	; set pointers and counters
	MOV  ESI, [EBP + 48]		; array1 start
	MOV  EDI, [EBP + 40]		; array2 start
	MOV  EAX, [EBP + 32]		; min

	MOV  ECX, [EBP + 36]		; max
	ADD  ECX, 1
	SUB  ECX, EAX				; ECX is now size of range [min, max]

	MOV  EDX, [EBP + 44]		; array1 size
	IMUL EDX, 4
	ADD  EDX, ESI				; EDX is end of array1
	
	MOV  EBX, 1
	
	; x = y = 0
	; for i in [min, max]:
	;	while i >= array1[x] and x < arrayLength:
	;		array2[y] += 1
	;		x += 1
	;	y += 1
_countLoop:
	CMP  EAX, [ESI]
	JL   _continue			
	CMP  ESI, EDX
	JGE  _continue
	ADD  [EDI], EBX
	ADD  ESI, 4
	JMP  _countLoop
_continue:
	ADD  EAX, 1	
	ADD  EDI, 4
	LOOP _countLoop

	RET  24

countList ENDP
;-----------------------------------------------------------------------------------------------------------------------------
; Name: displayMessage
; 
; Description: writes a message.
;
; Preconditions: string set to message.
;
; Postconditions: message written.  No register change.
;
; Receives: 
;		[EBP + 12]		= string address
;
; Returns: N/A
;-----------------------------------------------------------------------------------------------------------------------------
displayMessage PROC USES EDX EBP

	; set base pointer
	MOV  EBP, ESP

	; display message
	MOV  EDX, [EBP + 12]
	CALL WriteString

	RET  4

displayMessage ENDP

END main
