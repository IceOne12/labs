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

    mov ah, 10h 
    mov al, 3h 
    int 10h 

    mov ax, 0600h   
    mov bh, 07h 
    mov cx, 0000                    
    mov dx, 184Fh     
    int 10h                       
 
    mov dx, 0
    mov bh, 0
    mov ah, 02h
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

mWriteMatrix macro matrix,row,col 
local rowLoop, colLoop
    push ax
    push bx
    push cx 
    push si 

    xor bx,bx 
    mov cx, row 
rowLoop: 
    push cx 

    xor si,si 
    mov cx, col 
colLoop: 
    mov ax, matrix[bx][si]

    mWriteAX 

    xor ax,ax
    mWriteStr tab

    add si, 2
    loop colLoop 

    mWriteStr endl

    add bx, col 
    add bx, col
    pop cx
    loop rowLoop 

    pop si
    pop cx
    pop bx
    pop ax
endm

mReadMatrix macro matrix,row,col 
local rowLoop, colLoop
JUMPS
    push bx
    push cx 
    push si 

    xor bx,bx 
    mov cx, row 
rowLoop: 
    push cx 

    xor si,si 
    mov cx, col 
colLoop: 
    mReadAX buffer 4
    
    mov matrix[bx][si],ax
    add si, 2
    loop colLoop 

    mWriteStr endl

    add bx, col 
    add bx, col

    pop cx
    loop rowLoop 

    pop si
    pop cx
    pop bx
NOJUMPS
endm


mReverseMatrix macro matrix, row, col, resMatrix 
local rowLoop, colLoop
    push ax
    push bx
    push cx 
    push di
    push si

    mov di, 0                    
    mov cx, row 
rowLoop:
    push cx 
    mov si, 0                    
    mov cx, col
 
colLoop:
    push cx
    mov cx, row                   
    dec cx
    sub cx, di 
    mov ax, col       
    mul cx 

    mov cx, col 
    dec cx 
    sub cx, si 
    mov bx,cx                     
    add ax, bx                  
    shl ax, 1                    
    mov bx, ax
    mov ax, matrix[bx]
    mov cx,ax          
    
    mov ax, di                  
    mov bx, col           
    mul bx                      
    add ax, si                  
    shl ax, 1                    
    mov bx, ax
    mov ax,cx
    mov resMatrix[bx], ax       
    
    inc si
    pop cx
    loop colLoop

    inc di
    pop cx
    loop rowLoop

    pop si 
    pop di 
    pop cx 
    pop bx 
    pop ax 
endm

mMaxElementUpperandBottomdiagonal macro matrix, row, col, maxbot, maxupp 
local rowLoop, colLoop, upper_triangle, lower_triangle, skip
    push ax 
    push bx 
    push cx 
    push si 
    push di 
    push dx 

    mov maxbot, -32768
    mov maxupp, -32768
    
    xor dx,dx 
    xor di,di 
    xor bx, bx 
    mov cx, row 
rowLoop: 
    push cx 

    xor si,si 
    mov cx, col 
colLoop: 
    mov ax, matrix[bx][si]

    cmp si, di
    jg upper_triangle    
    jl lower_triangle 
    jmp skip   
  

upper_triangle:
    cmp ax, maxupp 
    jle skip
    mov maxupp, ax 
    jmp skip

lower_triangle:
    cmp ax, maxbot
    jle skip 
    mov maxbot, ax 
    jmp skip

skip:

    add si,2
    loop colLoop 

    add di, 2
    add bx, col 
    add bx, col 
    pop cx 
    loop rowLoop

    mov ax, maxupp
    mWriteAX
    mov ax, maxbot



    pop dx 
    pop di 
    pop si 
    pop cx 
    pop bx 
    pop ax 
endm
    
