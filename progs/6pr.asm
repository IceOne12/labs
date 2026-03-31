.model small
.stack 100h   
        
.data
    bool db 11100011b
    c db 0
    
.code                 
start:
    mov ax, @data 
    mov ds, ax

    mov dl,11110001b

    and dl,bool ; a
    
    or dl,bool ; b

    xor dl,bool ;c
    
    and dl,c ; d

    xor dl, 0FFh;e

    not dl ; f

    mov ax,4c00h
    int 21h

end start
