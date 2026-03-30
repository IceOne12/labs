import sys
import random

def main():
    print("-"*40)
    print("Enter the number in range 0-4, 1-4 for choise task, 0 for exit")
    print("1. Middle square metog")
    print("2. Kontrgruents metog")
    print("3. Fibonachi")
    print("4. Random from library Python")
    print("0. Exit")
    print("-"*40)
    x0 = 0.3050692026
    n = 199
    mas = [x0]
    choise =int(input())

    if (choise == 1):
        for i in range(n):
            frac = "{:.20f}".format(x0 * x0).split(".")[1]
            x0 = float("0." + frac[5:15])
            mas.append(x0)
        
        tot = len(mas)
        prob = 0.1
        expf = tot * prob
        
        counts = {str(d): 0 for d in range(10)}
        for val in mas:
            digit = "{:.10f}".format(val)[6]
            counts[digit] += 1
        
        csq = 0
        for d in range(10):
            obsf = counts[str(d)]
            csq += (obsf - expf) ** 2 / expf
        xero = 16.9
        
        if csq < xero:
            print("Is a good accidient",'xi^2=',csq)
        else:
            print("Is a bad accidient",'xi^2=',csq)
        print(counts)
        counts = {str(d): 0 for d in range(10)}
        for num in mas:
            element = "{:.10f}".format(num)[2]
            counts[element] += 1
        
        cq = 0
        for h in range(10):
            obsf = counts[str(h)]
            cq += (obsf - tot/10) ** 2 / (tot/10)
            
        if cq < xero:
            print("Is a good evenly",'xi^2=',cq)
        else:
            print("Is a bad evenly",'xi^2=',cq)
        print(counts)
        summ=0
        for m in range(len(mas)):
            summ+=mas[m]
        srznach=summ/len(mas)
        sumup,sumbot=0,0
        for kl in range(2,len(mas)):
            delimoe=(mas[kl]-srznach)*(mas[kl-1]-srznach)
            delitel=(mas[kl]-srznach)**2
            sumup+=delimoe
            sumbot+=delitel
        r=sumup/sumbot
        t=abs(r*((len(mas)-2)/(1-r**2))**0.5)
        if t<1.9702:
            print("Is a static independent",'t=',t,'r=',r)
        else:
            print("Is a not static independent",'t=',t,'r=',r)
        if len(mas)!= len(set(mas)):
            print("This array have a period")
        else:
            print("This array doesnt have a period")
        print('Array generated without middle square metod',mas)
        main()

    elif(choise == 2):
        x0 = 0.3050692026
        n = 200
        mas2=[]
        mas2.append(x0)
        m=2**31-1
        a=48271
        current_x=int(x0*m)
        for i in range(1,n):
            current_x=(a*current_x%m)
            norm_x=current_x/m
            mas2.append(norm_x)
        tot = len(mas2)
        prob = 0.1
        expf = tot * prob
        
        counts = {str(d): 0 for d in range(10)}
        for val in mas2:
            digit = "{:.10f}".format(val)[6]
            counts[digit] += 1
        
        csq = 0
        for d in range(10):
            obsf = counts[str(d)]
            csq += (obsf - expf) ** 2 / expf
        xero = 16.9
        
        if csq < xero:
            print("Is a good accidient",'xi^2=',csq)
        else:
            print("Is a bad accidient",'xi^2=',csq)
        print(counts)
        counts = {str(d): 0 for d in range(10)}
        for num in mas2:
            element = "{:.10f}".format(num)[2]
            counts[element] += 1
        
        cq = 0
        for h in range(10):
            obsf = counts[str(h)]
            cq += (obsf - tot/10) ** 2 / (tot/10)
            
        if cq < xero:
            print("Is a good evenly",'xi^2=',cq)
        else:
            print("Is a bad evenly",'xi^2=',cq)
        print(counts)
        summ=0
        for m in range(len(mas2)):
            summ+=mas2[m]
        srznach=summ/len(mas2)
        sumup,sumbot=0,0
        for kl in range(2,len(mas2)):
            delimoe=(mas2[kl]-srznach)*(mas2[kl-1]-srznach)
            delitel=(mas2[kl]-srznach)**2
            sumup+=delimoe
            sumbot+=delitel
        r=sumup/sumbot
        t=abs(r*((len(mas2)-2)/(1-r**2))**0.5)
        if t<1.9702:
            print("Is a static independent",'t=',t,'r=',r)
        else:
            print("Is a not static independent",'t=',t,'r=',r)
        if len(mas2)!= len(set(mas2)):
            print("This array have a period")
        else:
            print("This array doesnt have a period")    
        print('Array generated with kontrgruents metog',mas2)
        main()


    elif(choise == 3):
        alag=7
        b=10
        n=200
        x0=0.3050692026
        mas3=[]
        mas3.append(x0)
        m=2**31-1
        a=48271
        current_x=int(x0*m)
        for _ in range(9):
            current_x=(a*current_x%m)
            norm_x=current_x/m
            mas3.append(norm_x)
        for i in range(10,n):
            if mas3[i-alag]>=mas3[i-b]:
                mas3.append(mas3[i-alag]-mas3[i-b])
            else:
                mas3.append(mas3[i-alag]-mas3[i-b]+1)
        tot = len(mas3)
        prob = 0.1
        expf = tot * prob
        
        counts = {str(d): 0 for d in range(10)}
        for val in mas3:
            digit = "{:.10f}".format(val)[6]
            counts[digit] += 1
        
        csq = 0
        for d in range(10):
            obsf = counts[str(d)]
            csq += (obsf - expf) ** 2 / expf
        xero = 16.9
        
        if csq < xero:
            print("Is a good accidient",'xi^2=',csq)
        else:
            print("Is a bad accidient",'xi^2=',csq)
        print(counts)
        counts = {str(d): 0 for d in range(10)}
        for num in mas3:
            element = "{:.10f}".format(num)[2]
            counts[element] += 1
        
        cq = 0
        for h in range(10):
            obsf = counts[str(h)]
            cq += (obsf - tot/10) ** 2 / (tot/10)
            
        if cq < xero:
            print("Is a good evenly",'xi^2=',cq)
        else:
            print("Is a bad evenly",'xi^2=',cq)
        print(counts)
        summ=0
        for m in range(len(mas3)):
            summ+=mas3[m]
        srznach=summ/len(mas3)
        sumup,sumbot=0,0
        for kl in range(2,len(mas3)):
            delimoe=(mas3[kl]-srznach)*(mas3[kl-1]-srznach)
            delitel=(mas3[kl]-srznach)**2
            sumup+=delimoe
            sumbot+=delitel
        r=sumup/sumbot
        t=abs(r*((len(mas3)-2)/(1-r**2))**0.5)
        if t<1.9702:
            print("Is a static independent",'t=',t,'r=',r)
        else:
            print("Is a not static independent",'t=',t,'r=',r)
        if len(mas3)!= len(set(mas3)):
            print("This array have a period")
        else:
            print("This array doesnt have a period")
        print('Array generated without Fibonachi metod',mas3)
        main()


    elif(choise == 4):
        mas4=[random.random() for i in range(200)]
        tot = len(mas4)
        prob = 0.1
        expf = tot * prob
        
        counts = {str(d): 0 for d in range(10)}
        for val in mas4:
            digit = "{:.10f}".format(val)[6]
            counts[digit] += 1
        
        csq = 0
        for d in range(10):
            obsf = counts[str(d)]
            csq += (obsf - expf) ** 2 / expf
        xero = 16.9
        
        if csq < xero:
            print("Is a good accidient",'xi^2=',csq)
        else:
            print("Is a bad accidient",'xi^2=',csq)
        print(counts)
        counts = {str(d): 0 for d in range(10)}
        for num in mas4:
            element = "{:.10f}".format(num)[2]
            counts[element] += 1
        
        cq = 0
        for h in range(10):
            obsf = counts[str(h)]
            cq += (obsf - tot/10) ** 2 / (tot/10)
            
        if cq < xero:
            print("Is a good evenly",'xi^2=',cq)
        else:
            print("Is a bad evenly",'xi^2=',cq)
        print(counts)
        summ=0
        for m in range(len(mas4)):
            summ+=mas4[m]
        srznach=summ/len(mas4)
        sumup,sumbot=0,0
        for kl in range(2,len(mas4)):
            delimoe=(mas4[kl]-srznach)*(mas4[kl-1]-srznach)
            delitel=(mas4[kl]-srznach)**2
            sumup+=delimoe
            sumbot+=delitel
        r=sumup/sumbot
        t=abs(r*((len(mas4)-2)/(1-r**2))**0.5)
        if t<1.9702:
            print("Is a static independent",'t=',t,'r=',r)
        else:
            print("Is a not static independent",'t=',t,'r=',r)
        if len(mas4)!= len(set(mas4)):
            print("This array have a period")
        else:
            print("This array doesnt have a period")
        print("Array created by random",mas4)
        main()
    elif(choise == 0):
        return 0
    else:
        print("Enter the number in range 0-4")
        main()

main()
