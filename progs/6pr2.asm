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
.stack 100h           

.data
    initial db 'Vasilev V.V.' ,13,10,'$'
    result db 13,10,'Result:','$'
    prompt1 db 'a: ','$'
    prompt2 db 13,10,'b: 11110001 ','$' 
    p3 db 13,10,'3,5,7 bit=0, new a: ','$'
    p2 db 13,10,'a divide 4 = ','$'
    a db ?   
.code
start:
    mov ax,@data
    mov ds,ax
    xor ax,ax

    mWriteStr initial    
    mov al, 11100011b
    mov a,al
    mov bl,11110001b
    mWriteStr prompt1
    mWriteAX
    mWriteStr prompt2
    
    mov al,a
    and al, 01010111b
    xor ah,ah
    mov a,al
    mWriteStr p3
    mWriteAX
    
    mov al,a
    shr al,1
    shr al,1
    mov a,al
    mWriteStr p2
    mWriteAX
    
    mov al,a
    and al,bl ; 00010000
    mWriteStr result
    mWriteAX

    mov ax,4c00h
    int 21h

end start