mReadAX macro buffer,size
local input, startOfConvert, endOfConvert
    push bx
    push cx
    push dx
input:
    mov [buffer],size
    mov dx, offset [buffer]
    mov ah,0Ah
    int 21h

    mov ah,02h
    mov dl, 0Dh
    int 21h

    mov ah,02h
    mov dl, 0Ah
    int 21h 

    xor ah,ah
    cmp ah,[buffer][1]
    jz input
    
    xor cx,cx
    mov cl,[buffer][1]

    xor ax,ax
    xor bx,bx
    xor dx,dx
    mov bx, offset [buffer][2]
    cmp [buffer][2], '-'
    jne startOfConvert
    inc bx
    dec cl

startOfConvert:
    mov dx,10
    mul dx
    cmp ax,8000h
    jae input

    mov dl,[bx]
    sub dl,'0'

    add ax,dx
    cmp ax,8000h
    jae input

    inc bx
    loop startOfConvert

    cmp [buffer][2],'-'
    jne endOfConvert
    neg ax

endOfConvert:
    pop dx
    pop cx
    pop bx
endm mReadAX

mWriteAX macro                      
local convert, write
    push ax
    push bx
    push cx
    push dx
    push di

    mov cx,10
    xor di,di

    or ax,ax
    jns convert
    push ax

    mov dx, '-'
    mov ah,02h
    int 21h

    pop ax
    neg ax
    
convert:
    xor dx,dx
    
    div cx
    add dl,'0'
    inc di
    
    push dx
    
    or ax,ax
    jnz convert

write:
    pop dx

    mov ah,02h
    int 21h
    dec di
    jnz write

    pop di
    pop dx
    pop cx
    pop bx
    pop ax
endm mWriteAX

mCLS macro    
                   
    push ax           
    push bx 
    push cx 
    push dx 
           
    mov ah, 06h 
    mov al,0    
    mov bh, 07h 
    mov cx, 0000                    
    mov dx, 184Fh     
    int 10h                       
 
    pop dx            
    pop cx 
    pop bx 
    pop ax 
endm

mWriteStr macro string           
    push ax         
    push dx 
 
    mov ah, 09h     
    mov dx, offset string 
    int 21h 
 
    pop dx           
    pop ax 
endm

mCurs macro cols,rows
    push ax
    push bx
    push dx
    
    mov ah,02
    mov bh,00
    mov dh,cols
    mov dl,rows
    int 10h

    pop ax
    pop bx
    pop dx

endm
                         
.model small
.stack 1000h
.data
    input_buffer1 db 5,'?', 5 dup('?')
    input_buffer2 db 5,'?', 5 dup('?')
    menu1 db "1 - One-digit" , 13,10 , "$"
    menu2 db "2 - Two-digit" , 13,10 , "$"
    menu3 db "3 - Three-digit", 13,10, "$"
    select db "Select> $", 13,10
    prompt1 db "Enter a: $" , 13,10
    prompt2 db "Enter b: $" , 13,10
    result1 db "a>b, Result: $" , 13,10
    result2 db "a=b, Result: $" , 13,10
    result3 db "a<b, Result: $" , 13,10
    task db "Task: input the a and b. " , 13,10 ,'$'
    del db "Del in 0", 13,10, '$'
    task2 db "if a>b |x=(a-b)/a-3|", 13,10,'$'
    task3 db "if a=b |x=2|", 13,10,'$'
    task4 db "if a>b |x=(a**3 +1)/b|", 13,10,'$'
    a dw ?
    b dw ?
    x dw ?
    initial db "Vasilev V.V. " ,13,10, '$'
.code
start:
    mov ax, @data
    mov ds, ax
    
    mCLS

    mCurs 10,26    
    mWriteStr initial

    mCurs 11,26
    mWriteStr task

    mCurs 12,26
    mWriteStr task2

    mCurs 13,26
    mWriteStr task3

    mCurs 14,26
    mWriteStr task4
  
    mCurs 15,26
    mWriteStr menu1

    mCurs 16,26
    mWriteStr menu2
    
    mCurs 17,26
    mWriteStr menu3

trmore:
    mCurs 18,26
    mWriteStr select

    mov ah,01h
    int 21h

    cmp al,'1'
    je option1
    cmp al, '2'
    je option2
    cmp al,'3'
    je option3
    jmp trmore

option1: 
    jmp onedig
option2: 
    jmp twodig
option3:
    jmp threedig

onedig: 
    mCurs 19,26
    mWriteStr prompt1

    mReadAX input_buffer1,3
    mov a,ax

    mCurs 20,26
    mWriteStr prompt2

    mReadAX input_buffer2,3
    mov b,ax
    jmp srav

twodig: 
    mCurs 19,26
    mWriteStr prompt1

    mReadAX input_buffer1,4
    mov a,ax

    mCurs 20,26
    mWriteStr prompt2

    mReadAX input_buffer2,4
    mov b,ax
    jmp srav

threedig: 
    mCurs 19,26
    mWriteStr prompt1

    mReadAX input_buffer1,5
    mov a,ax

    mCurs 20,26
    mWriteStr prompt2

    mReadAX input_buffer2,5
    mov b,ax
    jmp srav

srav:
    mov ax,a
    mov bx,b
    cmp bx,0
    je c1
    cmp ax,b
    jg bol
    jl men
    jmp rav
c1:
    jmp er1
bol:
    mCurs 21,26
    mWriteStr result1

    mov ax,a
    sub ax,b
    mov bx,ax
    mov ax,a
    cmp ax, 3
    je c1
    sub ax,3
    xchg ax,bx
    cwd
    idiv bx
    xor dx,dx
    mov x,ax

    mWriteAX
    jmp exit

men:
    mCurs 21,26
    mWriteStr result3
 
    mov ax,a
    mov bx,a
    cwd
    imul bx
    xor dx,dx
    cwd
    imul a
    xor dx,dx
    add ax,1
    cwd
    idiv b
    xor dx,dx
    mov x,ax
    
    mWriteAX
    jmp exit
er1:
    mCurs 21,26
    mWriteStr del
    jmp exit
rav:
    mCurs 21,26
    mWriteStr result2

    mov ax,2
    mov x,ax
    
    mWriteAX
    jmp exit

exit:
    mov ax,4c00h
    int 21h
    
end start