.model small
.stack 100h

.data
   input_file    db 'lab7.txt', 0            
   FDescr        dw ?          
   output_file   db 'lab7new.txt', 0        
   FDescrNew     dw ?        
   short_prompt  db 'Shortest string: $'
   long_prompt   db 'Longest string: $'
   newline       db 13, 10, '$'
   
   error_open    db 13, 10, 'File was not open!$'
   error_create  db 13, 10, 'File was not created!$'
   error_read    db 13, 10, 'File was not read!$'
   error_write   db 13, 10, 'Error in writing in the file!$'
   error_empty   db 13, 10, 'File is empty!$'
   error_founded db 13, 10, 'File was not founded!$'
   initial db 13,10,'Spasenova E.S.',13,10,'$'

   buffer        db 10000 dup(?)            
   
   ; Буферы для строк
   current_line  db 256 dup(?)              
   shortest_line db 256 dup(?)              
   longest_line  db 256 dup(?)              
   
   ; Переменные для работы со строками
   current_len   dw 0
   shortest_len  dw 65535    ; начальное максимальное значение
   longest_len   dw 0
   
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
   
   ; Открытие исходного файла
   mov ah, 3Dh
   mov al, 0              
   mov dx, offset input_file
   xor cx, cx
   int 21h
   jnc M1
   jmp Er1

M1:
   mov FDescr, ax        
   
   ; Создание нового файла
   mov ah, 3Ch
   xor cx, cx
   mov dx, offset output_file
   int 21h
   jnc M1_1
   jmp Er3
   
M1_1:
   mov FDescrNew, ax      
   
   ; Начинаем чтение файла
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
   
   ; Проверка на конец строки
   cmp al, 13
   je handle_cr
   cmp al, 10
   je handle_lf
   
   ; Добавляем символ в текущую строку
   mov bx, current_len
   mov current_line[bx], al
   inc current_len
   jmp read_loop

handle_cr:
   ; Просто пропускаем CR
   jmp read_loop

handle_lf:
   ; Когда встречаем LF (10), обрабатываем строку
   cmp current_len, 0
   je read_loop  ; Пропускаем пустые строки
   
   ; Завершаем текущую строку
   mov bx, current_len
   mov byte ptr current_line[bx], '$'
   
   ; Сравниваем с самой короткой строкой
   mov ax, current_len
   cmp ax, shortest_len
   jae check_longest
   
   ; Нашли более короткую строку - копируем
   mov shortest_len, ax
   mov cx, current_len
   mov si, offset current_line
   mov di, offset shortest_line
copy_short:
   mov al, [si]
   mov [di], al
   inc si
   inc di
   loop copy_short
   mov byte ptr [di], '$'
   
check_longest:
   ; Сравниваем с самой длинной строкой
   mov ax, current_len
   cmp ax, longest_len
   jbe reset_current
   
   ; Нашли более длинную строку - копируем
   mov longest_len, ax
   mov cx, current_len
   mov si, offset current_line
   mov di, offset longest_line
copy_long:
   mov al, [si]
   mov [di], al
   inc si
   inc di
   loop copy_long
   mov byte ptr [di], '$'
   
reset_current:
   ; Сбрасываем текущую строку для следующей
   mov current_len, 0
   jmp read_loop

end_of_file:
   ; Обработка последней строки (если файл не заканчивается на LF)
   cmp current_len, 0
   je finish_processing
   
   ; Завершаем текущую строку
   mov bx, current_len
   mov byte ptr current_line[bx], '$'
   
   ; Сравниваем с самой короткой строкой
   mov ax, current_len
   cmp ax, shortest_len
   jae check_longest_last
   
   mov shortest_len, ax
   mov cx, current_len
   mov si, offset current_line
   mov di, offset shortest_line
copy_short_last:
   mov al, [si]
   mov [di], al
   inc si
   inc di
   loop copy_short_last
   mov byte ptr [di], '$'
   
check_longest_last:
   mov ax, current_len
   cmp ax, longest_len
   jbe finish_processing
   
   mov longest_len, ax
   mov cx, current_len
   mov si, offset current_line
   mov di, offset longest_line
copy_long_last:
   mov al, [si]
   mov [di], al
   inc si
   inc di
   loop copy_long_last
   mov byte ptr [di], '$'

finish_processing:
   ; Проверяем, есть ли строки в файле
   cmp shortest_len, 65535
   je op1
   
   ; Выводим информацию об авторе
   mov dx, offset initial
   print_string
   
   ; Выводим самую короткую строку
   mov dx, offset short_prompt
   print_string
   mov dx, offset shortest_line
   print_string
   mov dx, offset newline
   print_string
   
   ; Выводим самую длинную строку
   mov dx, offset long_prompt
   print_string
   mov dx, offset longest_line
   print_string
   mov dx, offset newline
   print_string
   
   ; Записываем строки в новый файл
   ; Сначала самую короткую строку
   mov ah, 40h
   mov bx, FDescrNew
   mov cx, shortest_len
   mov dx, offset shortest_line
   int 21h
   jnc write_short_ok
   jmp Er4
op1:
    jmp file_empty
write_short_ok:
   ; Добавляем перенос строки
   mov ah, 40h
   mov bx, FDescrNew
   mov cx, 2
   mov dx, offset newline
   int 21h
   jnc write_newline1_ok
   jmp Er4
   
write_newline1_ok:
   ; Теперь самую длинную строку
   mov ah, 40h
   mov bx, FDescrNew
   mov cx, longest_len
   mov dx, offset longest_line
   int 21h
   jnc write_long_ok
   jmp Er4
   
write_long_ok:
   ; Добавляем перенос строки
   mov ah, 40h
   mov bx, FDescrNew
   mov cx, 2
   mov dx, offset newline
   int 21h
   jnc write_newline2_ok
   jmp Er4
   
write_newline2_ok:
   jmp close_files

file_empty:
   mov dx, offset error_empty
   print_string
   jmp close_files

close_files:
   mov ah, 3Eh
   mov bx, FDescr
   int 21h

   mov ah, 3Eh
   mov bx, FDescrNew
   int 21h

   jmp Exit

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