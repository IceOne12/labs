import time
import pandas as pd
def lin(mas,sn):
    for i in range(len(mas)):
        if mas[i]==sn:
            return i
def binary(mas,sn):
    first=0
    last=len(mas)-1
    index=-1
    while first<=last and index==-1:
        mid=(first+last)//2
        if mas[mid]==sn:
            index=mid
        else:
            if sn<mas[mid]:
                last=mid-1
            else:
                first=mid+1
                       
    return index
def main():
    print("-"*50)
    print('1.Line search')
    print('2.Binary search')
    print('0.Exit')
    print("-"*50)
    choice=int(input("Choice the search method --> "))
    if choice == 1:
        mas=[118,118,110,114,94,99,119,101,116,116,117,118,118,119,115,111,99,110,110,111,104,120,110,114,99,118,98,101,116,116,105,120,120,116,119,104,113,111,99,100,116,118,113,101,105,118,118,109,118,109,109,116,99,114,113]
        sn=116
        ind_mas=[]
        for i in range(5):
            start=time.perf_counter()*1000
            index=lin(mas,sn)
            end=time.perf_counter()*1000
            ind_mas.append(index)
            sn +=1
            print(sn-1, index, end-start,'ms')
        df=pd.DataFrame(ind_mas)
        df.to_excel('res1.xlsx')
        main()
    elif choice==2:
        mas=[118,118,110,114,94,99,119,101,116,116,117,118,118,119,115,111,99,110,110,111,104,120,110,114,99,118,98,101,116,116,105,120,120,116,119,104,113,111,99,100,116,118,113,101,105,118,118,109,118,109,109,116,99,114,113]
        mas.sort()
        sn=116
        ind_mas=[]
        for i in range(5):
            start=time.perf_counter()*1000
            index=binary(mas,sn)
            end =time.perf_counter()*1000
            ind_mas.append(index)
            sn +=1
            print(sn-1,index, end-start, 'ms')
        df=pd.DataFrame(ind_mas)
        df.to_excel('res2.xlsx')
        main()
    elif choice==0: return 0
    else:
        print("Enter the number in range 0-2")
        main()

main()
