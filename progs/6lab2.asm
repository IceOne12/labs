.686
.model flat, C        

.data
    EXTRN C y: dword
    EXTRN C x: dword
    
    
    halfone dd 0.5
    three dd 3.0
    
.code
    public  l62
    l62 proc far
        finit
        
        
        fld x
        ftst 
        ; x 0
        jl rst 
        fld halfone
        fcomip st(0), st(1)
        ; 0.5 x
        jl third
        jmp second

        rst:
            fld x
            fcos
            fmul st(0),st(0)
            jmp exit
        
        third:
            fld x 
            fptan 
            fmul st(0), st(0)
            jmp exit 
        
        second:
            fld x
            fld1 
            fscale
            fld three
            fadd st(1),st(0)
            fld st(1)
            jmp exit             

        exit:
            fstp y
        
            retn
    l62 endp

end 