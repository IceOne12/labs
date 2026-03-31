.model tiny
.code
org 100h

start:
    jmp main
    
    input_file    db 'lab7.txt', 0
    output_file   db 'lab7new.txt', 0
    prompt        db '4-th string: $'
    newline       db 13, 10, '$'
    
    handle        dw ?
    handle_new    dw ?
    file_size     dw ?
    line_count    dw 1
    line4_index   dw 0
    
    buffer        db 10000 dup(?)
    line4_buffer  db 256 dup(?)

main:
    mov ah, 3Dh
    mov al, 0
    lea dx, input_file
    int 21h
    jnc open_ok
    jmp open_error     
    
open_ok:
    mov handle, ax
    
    mov ah, 3Fh
    mov bx, handle
    mov cx, 10000
    lea dx, buffer
    int 21h
    jnc read_ok
    jmp read_error     
    
read_ok:
    mov file_size, ax
    
    mov ah, 3Eh
    mov bx, handle
    int 21h
    
    lea si, buffer
    mov cx, file_size
    mov line_count, 1
    mov line4_index, 0
    
find_line4:
    cmp cx, 0
    je file_end
    
    mov al, [si]
    inc si
    dec cx
    
    cmp al, 13
    je handle_cr
    cmp al, 10
    je handle_lf
    
    cmp line_count, 4
    jne find_line4
    
    mov bx, line4_index
    mov line4_buffer[bx], al
    inc line4_index
    jmp find_line4
    
handle_cr:
    cmp cx, 0
    je check_line_end
    cmp byte ptr [si], 10
    jne check_line_end
    inc si
    dec cx
    
check_line_end:
    cmp line_count, 4
    je continue_search
    inc line_count
    jmp find_line4
    
handle_lf:
    cmp line_count, 4
    je continue_search
    inc line_count
    jmp find_line4
    
continue_search:
    jmp find_line4
    
file_end:
    cmp line_count, 4
    jge process_line4     
    jmp lines_error       
    
process_line4:
    mov cx, line4_index
    jcxz lines_error      
    
    lea si, line4_buffer
    
convert:
    mov al, [si]
    cmp al, 'A'
    jb next
    cmp al, 'Z'
    ja next
    add al, 32
    mov [si], al
next:
    inc si
    loop convert
    
    mov ah, 09h
    lea dx, prompt
    int 21h
    
    mov bx, line4_index
    mov byte ptr line4_buffer[bx], '$'
    
    lea dx, line4_buffer
    int 21h
    
    lea dx, newline
    int 21h
    
    mov ah, 3Ch
    mov cx, 0
    lea dx, output_file
    int 21h
    jnc create_ok
    jmp write_error
    
create_ok:
    mov handle_new, ax
    
    mov ah, 40h
    mov bx, handle_new
    mov cx, line4_index
    lea dx, line4_buffer
    int 21h
    jnc write_ok
    jmp write_error2
    
write_ok:
    mov ah, 3Eh
    mov bx, handle_new
    int 21h
    
    mov ax, 4C00h
    int 21h


open_error:
    mov ah, 09h
    mov dx, offset error_open
    int 21h
    jmp exit_err
    
read_error:
    mov ah, 09h
    mov dx, offset error_read
    int 21h
    jmp exit_err
    
lines_error:
    mov ah, 09h
    mov dx, offset error_lines
    int 21h
    jmp exit_err
    
write_error:
    mov ah, 09h
    mov dx, offset error_write
    int 21h
    jmp exit_err2
    
write_error2:
    cmp handle_new, 0
    je no_close
    mov ah, 3Eh
    mov bx, handle_new
    int 21h
no_close:
    mov ah, 09h
    mov dx, offset error_write
    int 21h
    
exit_err2:
    mov ax, 4C01h
    int 21h

exit_err:
    mov ax, 4C01h
    int 21h

error_open    db 'File open error!$'
error_read    db 'File read error!$'
error_write   db 'Write error!$'
error_lines   db 'Less than 4 lines!$'

end start