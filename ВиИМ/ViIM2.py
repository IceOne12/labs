import sys
import numpy as np
from math import *
def main():
    print("-"*50)
    print("0. Exit")
    print("1. Equal mesure")
    print("2. Exponential low")
    print("3. Box-Muller method")
    print("4. Central limit teorems")
    print("-"*50)
    choise=int(input("Enter the number from keyboard 0-4 --> "))
    if choise==1:
        x0 = 0.3050692026
        n = 100
        mas2=[]
        mas2.append(x0)
        m=2**31-1
        a=48271
        al=5-12.5
        b=5+0.5
        current_x=int(x0*m)
        for i in range(1,n):
            current_x=(a*current_x%m)
            norm_x=current_x/m
            mas2.append(norm_x)
        mas=[]
        for i in range(n):
            x_i=al+(b-al)*mas2[i]
            mas.append(x_i)
        ranges=[-7.5,-6.2,-4.9,-3.6,-2.3,-1.0,0.3,1.6,2.9,4.2,5.5]
        counts, bin_edges=np.histogram(mas, bins=ranges)
        print("Counts numerate in other diapozons",counts)
        print("Diapozons for counting",bin_edges)
        cq = 0
        xero=16.9
        tot=len(mas)
        for h in range(10):
            obsf = counts[h]
            cq += (obsf - tot/10) ** 2 / (tot/10)
            
        if cq < xero:
            print("Is a good evenly",'xi^2=',cq)
        else:
            print("Is a bad evenly",'xi^2=',cq)
        print("Numbers generated in range",al,';',b, '\nArray:',mas)
        main()
    elif(choise == 2):
        x0 = 0.3050692026
        n = 20
        t=4000+100*3+20*5
        l=1/t
        endt=5000
        mas2=[]
        mas2.append(x0)
        m=2**31-1
        a=48271
        current_x=int(x0*m)
        for i in range(1,n*3):
            current_x=(a*current_x%m)
            norm_x=current_x/m
            mas2.append(norm_x)
        cnt=0
        for j in range(3):
            mas=[]
            counter=0
            for i in range(n*j,n*(j+1)):
                x_i=-1/l*log(mas2[i])
                if x_i<endt:
                    counter +=1
                mas.append(x_i)
            cnt+=counter
            
            print("\n№ tests is",j+1,"\nTime working",mas,"\nNeed to restart:",counter)
        print('Middle number needed restarting is',cnt/3)
        main()
    elif(choise==3):
        x0 = 0.3050692026
        n = 100
        mas2=[]
        mas2.append(x0)
        m=2**31-1
        a=48271
        d=5
        sigma=5/10
        s2=1
        mas=[]
        ct=0
        current_x=int(x0*m)
        for i in range(1,(n+1)*3):
            current_x=(a*current_x%m)
            norm_x=current_x/m
            mas2.append(norm_x)
        srr=0
        print("Middle diametr=",d,"mm;")
        print("Middle square defects sigma=",sigma,'mm')
        for j in range(3):
            mas=[]
            ct=0
            for i in range(n*j,n*(j+1),2):
                z=sqrt(-2*log(mas2[i]))*cos(2*pi*mas2[i+1])
                z=d+sigma*z
                if (abs(z-d)>s2):
                    ct+=1
                    mas.append(z)
                z=sqrt(-2*log(mas2[i]))*sin(2*pi*mas2[i+1])
                z=d+sigma*z
                if (abs(z-d)>s2):
                    ct+=1
                    mas.append(z)
            srr+=ct
            print("№ of tests",j+1,"\nSize of bad details:",mas,"\nThey count is",ct)               
        print("Middle number of bad details is",srr/3)
        main()
    elif(choise==4):
        x0 = 0.3050692026
        n = 365*12
        days=365
        mas2=[]
        mas2.append(x0)
        m=2**31-1
        a=48271
        sigma=10
        norm_visit=100
        min_visit=120
        summ=0
        mas=[]
        cnte=0
        current_x=int(x0*m)
        for i in range(1,n):
            current_x=(a*current_x%m)
            norm_x=current_x/m
            mas2.append(norm_x)
        for i in range(days):
            summ=0
            for j in range(i*12,12+i*12):
                summ+=mas2[j]
            x=-6+summ
            z=int(norm_visit+sigma*x)
            if z>=120:
                cnte+=1
                mas.append(z)
        print("Visit not less the 120 - ",cnte,'times:',mas)
        main()
    elif(choise==0): return 0
    else:
        print("Type the number from keyboard from range 0-4!!")
        main()
main()
