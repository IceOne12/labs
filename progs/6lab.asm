.8087
.model flat, C        

.data
    EXTRN C result: dword
    EXTRN C x: dword
    
    
    two dd 2.0
    one dd 1.0
    pi_div_6 dd 0.5235987756  
    two_pi dd 6.2831853072    
    
.code
    PUBLIC C _6lab_as
    _6lab_as proc far
        finit
        
        
        fld x
        
        ; sqrt (x^4 - 1)

        fld st(0)             
        fmul st(0), st(0)     
        fmul st(0), st(0)     
        fsub one              
        fsqrt                 
        
        ;log2(sqrt(x^4 - 1))

        fld1                  
        fld st(1)             
        fyl2x                 
        
        
        fst st(1)             
        
        ;  2 * sin(x) * log2(sqrt(x^4 - 1)) + 1

        fld x                
        fsin                  
        fmul two              
        fmul st(0), st(2)     
        fadd one              
        
        
        fld x                 
        fmul two              
        fsin                  
        fadd pi_div_6         
        fld two_pi            
        fdiv st(0), st(1)     
        
        
        fdivp st(1), st(0)    

        ;arctg^2(log2(sqrt(x^4 - 1)))

        fld st(2)             
        fld1                  
        fpatan                
        fmul st(0), st(0)     
        
        
        fsubp st(1), st(0)    
        
        
        fstp result
        
        retn
    _6lab_as endp

end 