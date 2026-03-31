                  
.model small
.486
.stack 1000h
.data
    endl db 13,10,'$'
    tab db 09,'$'
    space db ' $'
    prompt1 db "Enter cols of matrix: $"
    prompt2 db "Enter rows of matrix: $"
    promptEl db 'Enter the matrix elements element by element: ',13,10,'$'
    menu1 db 'Home Tasks Vasilev V.V. 2 version',13,10,'corresponding key on the keyboard','$'
    menu0 db '0. Exit from program ',13,10,'$'
    menu5 db '1. Write matrix',13,10,'$'
    menu6 db '2. Show matrix',13,10,'$'
    menu2 db '3. First tasks: Reverse the order of the elements',13,10,'$'
    menu3 db '4. Second tasks: Cheack if the 2 row and the 2 column are equal',13,10,'$'
    menu4 db '5. Third tasks: What the max element in the upper triangle and bottom triangle',13,10,'$'
    resb1 db 'No, they not equal',13,10,'$'
    resb2 db 'Yes, they equal',13,10,'$'
    newmatrix db 'Martix with reversed elements and rows',13,10,'$'
    maxelupper db 'Max element in the upper triangle is $'
    maxelbottom db 'Max element in the bottom triangle is $'
    buffer db 20 dup(?)
    rows dw ?
    cols dw ?
    i dw ?
    maxelbot dw -32000
    maxelup dw -32000
    currentMatrix dw 100 dup(0)
    reversedMatrix dw 100 dup(0)
.code
start:
    mov ax, @data
    mov ds, ax
    
    include macros.asm

menu:
    mCLS

    mWriteStr menu1
    mWriteStr endl
    mWriteStr endl 

    mWriteStr menu5
    mWriteStr menu6
    mWriteStr menu2
    mWriteStr menu3
    mWriteStr menu4
    mWriteStr menu0

    mov ah, 00h
    int 16h

    cmp al,'1'
    je wrm 

    cmp al,'2'
    je shm 

    cmp al,'3'
    je task1

    cmp al,'4'
    je task2

    cmp al,'5'
    je task3

    cmp al,'0'
    je exit

    jmp menu
wrm:
    mCLS
    mWriteStr prompt1
    mReadAX buffer, 2
    mov cols,ax
    mWriteStr endl

    mWriteStr prompt2
    mReadAX buffer, 2
    mov rows,ax
    mWriteStr endl

    mWriteStr promptEl

    mReadMatrix currentMatrix, rows, cols
    mov ah, 07h
    int 21h
    jmp menu

shm:
    mCLS
    mWriteMatrix currentMatrix, rows, cols
    
    mov ah, 07h
    int 21h
    jmp menu

task1:
    mCLS
    mWriteStr prompt1
    mReadAX buffer, 2
    mov cols,ax
    mWriteStr endl

    mWriteStr prompt2
    mReadAX buffer, 2
    mov rows,ax
    mWriteStr endl

    mWriteStr promptEl

    mReadMatrix currentMatrix, rows, cols 
    
    mWriteMatrix currentMatrix, rows, cols 
    mWriteStr endl 
    mWriteStr endl 
    mReverseMatrix currentMatrix, rows, cols, reversedMatrix
    mWriteMatrix reversedMatrix, rows, cols 

    mov ah, 07h
    int 21h
    jmp menu 

task2: 
    mCLS
    mWriteStr prompt1
    mReadAX buffer, 2
    mov cols,ax
    mWriteStr endl

    mWriteStr prompt2
    mReadAX buffer, 2
    mov rows,ax
    mWriteStr endl

    mWriteStr promptEl

    mReadMatrix currentMatrix, rows, cols 
    
    mWriteMatrix currentMatrix, rows, cols 
    mWriteStr endl 
    mWriteStr endl

    xor bx,bx
    mov cx,cols 
    mov i, 0

rowLoop:
    mov ax, 1 
    mov bx, rows 
    mul bx 
    add ax, i 
    shl ax, 1
    mov di, ax 
    mov ax, [currentMatrix+di]  
    
    push ax  
    
    mov ax, i 
    mov bx, rows 
    mul bx 
    add ax, 1
    shl ax, 1
    mov di, ax 
    mov bx, [currentMatrix+di]  
    
    pop ax   
    
    cmp ax, bx 
    jnz noEqual
    
    inc i
    loop rowLoop
    
    jmp YeEq

YeEq:
    mWriteStr resb2
    mov ah, 07h
    int 21h
    jmp menu

noEqual:
    mWriteStr resb1
    mov ah, 07h
    int 21h
    jmp menu

task3:
    mCLS
    mWriteStr prompt1
    mReadAX buffer, 2
    mov cols,ax
    mWriteStr endl

    mWriteStr prompt2
    mReadAX buffer, 2
    mov rows,ax
    mWriteStr endl

    mWriteStr promptEl

    mReadMatrix currentMatrix, rows, cols 
    
    mWriteMatrix currentMatrix, rows, cols 
    mWriteStr endl 
    mWriteStr endl
    mWriteStr maxelupper
    mMaxElementUpperandBottomdiagonal currentMatrix, rows, cols, maxelbot, maxelup
    mWriteStr endl
    mWriteStr maxelbottom
    mov ax, maxelbot
    mWriteAX
    
    mov ah,07h
    int 21h
    jmp menu 


exit:
    mov ax,4c00h
    int 21h
    
end start