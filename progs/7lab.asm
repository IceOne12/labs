.model small
.stack 100h

.data
    input_file    db 'lab7.txt', 0            
    FDescr        dw ?          
    output_file   db 'lab7new.txt', 0         
    FDescrNew     dw ?        
    line4_prompt  db '4-th string(after rebuilding): $'
    newline       db 13, 10, '$'
    
    error_open    db 13, 10, 'File was not open!$'
    error_create  db 13, 10, 'File was not created!$'
    error_read    db 13, 10, 'File was not read!$'
    error_write   db 13, 10, 'Error in writing in the file!$'
    error_lines   db 13, 10, 'File have less a 4 strings!$'
    error_founded db 13, 10, 'File was not founded!$'
    initial db 13,10,'Vasilev V.V.',13,10,'$'

    buffer        db 10000 dup(?)             
    line4_buffer  db 256 dup(?)               
    
    index         dw 0
    line_count    dw 1
    line4_index   dw 0                                              
    temp_char     db ?                        

.code
print_string macro
    mov ah, 09h
    int 21h
endm

start:
    mov ax, @data
    mov ds, ax
    mov es, ax
    

    mov ah, 3Dh
    mov al, 0              
    mov dx, offset input_file
    xor cx, cx 
    int 21h 
    jnc M1
    jmp Er1

M1:
    mov FDescr, ax         
    
    
    mov ah, 3Ch
    xor cx, cx 
    mov dx, offset output_file
    int 21h
    jnc M1_1
    jmp Er3
    
M1_1:
    mov FDescrNew, ax      
    
    
read_loop:
    
    mov ah, 3Fh
    mov bx, FDescr
    mov cx, 1              
    mov dx, offset temp_char 
    int 21h
    jnc M2
    jmp Er2
    
M2:
    
    cmp ax, 0
    je end_of_file
    
    
    mov al, temp_char      
    
    
    cmp al, 13             
    je handle_endline
    cmp al, 10             
    je handle_endline
    
    
    cmp line_count, 4
    jne skip_char          
    
    
    mov di, line4_index
    mov line4_buffer[di], al  
    inc line4_index
    jmp read_loop
    
skip_char:
    jmp read_loop

handle_endline:
    
    cmp line_count, 4
    jne not_line4
    
    
    cmp al, 13             
    je read_loop           
    
    
    mov di, line4_index
    mov byte ptr line4_buffer[di], '$'  
    inc line_count                      
    jmp read_loop                       
    
not_line4:
    
    cmp al, 10             
    jne read_loop
    inc line_count
    jmp read_loop

end_of_file:
    
    cmp line_count, 4
    jl file_too_short
    
    
    cmp line4_index, 0
    je file_too_short
    
    
    mov di, line4_index
    mov byte ptr line4_buffer[di], '$'
    
    
    mov cx, line4_index
    mov si, offset line4_buffer
convert_loop:
    mov al, [si]
    cmp al, 'A'
    jb next_char_conv
    cmp al, 'Z'
    ja next_char_conv
    add al, 32              
    mov [si], al
next_char_conv:
    inc si
    loop convert_loop
    
    
    mov ah, 40h
    mov bx, FDescrNew
    mov cx, line4_index     
    mov dx, offset line4_buffer
    int 21h
    jnc M3
    jmp Er4
    
M3:
    
    mov dx, offset initial
    print_string

    mov dx, offset line4_prompt
    print_string
    
    mov dx, offset line4_buffer
    print_string
    
    mov dx, offset newline
    print_string
    
close_files:
    mov ah, 3Eh 
    mov bx, FDescr
    int 21h

    mov ah, 3Eh
    mov bx, FDescrNew
    int 21h

    jmp Exit

file_too_short:
    mov dx, offset error_lines
    print_string
    jmp close_files

Er1:
    cmp ax, 02h
    jne M6
    mov dx, offset error_founded
    print_string 
    jmp Exit 
M6:
    mov dx, offset error_open
    print_string
    jmp Exit

Er2:
    mov dx, offset error_read
    print_string
    jmp close_files

Er3:
    mov dx, offset error_create
    print_string
    jmp close_files 
    
Er4:
    mov dx, offset error_write
    print_string
    jmp close_files 
    
Exit:
    mov ah, 07h
    int 21h

    mov ax, 4C00h
    int 21h

end start