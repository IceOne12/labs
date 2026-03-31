mWriteAX macro                      
local convert, write
    push ax
    push bx
    push cx
    push dx
    push di

    mov cx,2
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

mWriteStr macro message
    push ax         
    push dx 
 
    mov ah, 09h     
    mov dx, offset message 
    int 21h 
 
    pop dx           
    pop ax 
endm mWriteStr


.model small
.stack 1000h           
.data
    initial db 'Spasyenova E.S.' ,13,10,'$'
    result db 13,10, 'Result:','$'
    text1 db 'a: ','$'

    t3 db 13,10,'change 3 and 7 digit, new a: ','$'
    t4 db 13,10,'a divide 8 = ','$'
    a db ?   

.code
start:
    mov ax,@data
    mov ds,ax
    xor ax,ax
    ;00111100
    ;10110100
    ;00010110
    ;00111000
    ;00111110
    mWriteStr initial    
    mov al, 00111100b ;60
    mov a, al
    mWriteStr text1
    mWriteAX

    mov bl, al      
    and bl, 00001000b
    xor dx,dx 
    mov cl, 3 
    shr bl, cl
       

    mov dl, al        
    and dl, 10000000b
    xor dx,dx 
    mov cl, 7
    shr dl, cl  
    
    cmp bl, dl

    je skip
    mov al,a  
    xor al, 10001000b
    mWriteStr t3 
    mWriteAX

skip:
    shr al,1
    shr al,1
    shr al,1
    mov bl, 56

    mWriteStr t4 
    mWriteAX

    or al,bl

    mWriteStr result
    mWriteAX

    mov ax,4c00h
    int 21h

end start
 
