.model small
.stack 100h

.data
    old_1c        dd  0        
    delay         dw  29       
    show_space    db  0        
    symbol        db  'V'      
    exit_flag     db  0
    timer_counter dw  0
    pos           dw  1820     
    msg1 db 'Enter 1 to 9 for change speed$'
    msg2 db 'Vasilev V.V.$'
.code
start:
    mov ax, @data
    mov ds, ax

    mov ax, 351Ch
    int 21h
    mov word ptr [old_1c], bx
    mov word ptr [old_1c+2], es

    mov ax, 251Ch
    mov dx, offset new_1c
    push ds
    push cs
    pop ds
    int 21h
    pop ds

    mov ax, 0B800h
    mov es, ax
    mov di, 0
    mov cx, 2000
    mov ax, 0720h  
clear:
    mov es:[di], ax
    add di, 2
    loop clear
mov ah, 02h
mov bh, 0
mov dh, 0    
mov dl, 0    
int 10h

mov ah, 09h
lea dx, msg1
int 21h

mov ah, 02h
mov bh, 0
mov dh, 1    
mov dl, 0    
int 10h

mov ah, 09h
lea dx, msg2
int 21h
main_loop:
    cmp [exit_flag], 1
    je restore_exit
    
    mov cx, 0FFh
delay_main:
    nop
    loop delay_main
    
    jmp main_loop

restore_exit:
    lds dx, [old_1c]
    mov ax, 251Ch
    int 21h
    
    mov ax, 4C00h
    int 21h

new_1c proc far
    push ax
    push bx
    push cx
    push dx
    push di
    push ds
    push es
    
    mov ax, @data
    mov ds, ax
    
    mov ah, 01h
    int 16h
    jz no_key
    
    mov ah, 00h
    int 16h
    
    cmp al, '0'
    jne check_digit
    mov [exit_flag], 1
    jmp no_key
    
check_digit:
    cmp al, '1'
    jb no_key
    cmp al, '9'
    ja no_key
    
    sub al, '0'
    xor ah, ah
    mov bl, 29
    mul bl
    mov [delay], ax
    mov [timer_counter], 0  
    
no_key:
    inc [timer_counter]
    mov ax, [timer_counter]
    cmp ax, [delay]
    jb exit_handler
    
    mov [timer_counter], 0
    
    mov ax, 0B800h
    mov es, ax
    mov di, [pos]           
    
    cmp [show_space], 0
    jne put_space_now
    
    mov al, [symbol]
    mov ah, 0Eh             
    jmp write_now
    
put_space_now:
    mov di, [pos]
    mov al, ' '
    mov ah, 0Eh             
    
write_now:
    mov es:[di], ax
    
    xor [show_space], 1
    
exit_handler:
    pop es
    pop ds
    pop di
    pop dx
    pop cx
    pop bx
    pop ax
    iret
new_1c endp

end start