import time
import pandas as pd
from itertools import *
import string
apb=string.ascii_letters
apb1='qwertydf'
alphabet=string.digits+apb1
alp=string.digits
alp1='12'
def brute_force(alphabet, min_len, max_len):
    joiner = ''.join
    for cur_len in range(min_len, max_len + 1):
        yield from map(joiner, product(alphabet, repeat=cur_len))

def main():
    print("-"*50)
    print('1.Decart multing')
    print('2.Permutations')
    print('3.Combinations')
    print('4.Combinations with replacement')
    print('5.Brut Force Keyword')
    print('0.Exit')
    print("-"*50)
    choice=int(input("Choice the method of products --> "))
    if choice == 1:
        start=time.perf_counter()*1000
        pr=list(product(alp,apb))
        end=time.perf_counter()*1000
        print(pr)
        print('Time in ms:', end-start)
        df=pd.DataFrame(pr)
        df.to_excel('resva3.xlsx')
        start=time.perf_counter()*1000
        pr=list(product(alp,apb1,repeat=2))
        end=time.perf_counter()*1000
        print('Decart multing with repeat:',pr)
        print('Time in ms:', end-start)
        df=pd.DataFrame(pr)
        df.to_excel('resva3_2.xlsx')
        main()
    elif choice==2:
        start=time.perf_counter()*1000
        pr=list(permutations(apb1))
        end=time.perf_counter()*1000
        print(pr)
        print('Time in ms:', end-start)
        df=pd.DataFrame(pr)
        df.to_excel('resva3_3.xlsx')
        start=time.perf_counter()*1000
        pr=list(permutations(apb,3))
        end=time.perf_counter()*1000
        print('Permutations with length 5', pr)
        print('Time in ms:', end-start)
        df=pd.DataFrame(pr)
        df.to_excel('resva3_4.xlsx')
        main()
    elif choice==3:
        start=time.perf_counter()*1000
        pr=list(combinations(alp,4))
        end=time.perf_counter()*1000
        print(pr)
        print('Time in ms:', end-start)
        df=pd.DataFrame(pr)
        df.to_excel('resva3_5.xlsx')
        main()
    elif choice==4:
        start=time.perf_counter()*1000
        pr=list(combinations_with_replacement(apb,4))
        end=time.perf_counter()*1000
        print(pr)
        print('Time in ms:', end-start)
        df=pd.DataFrame(pr)
        df.to_excel('resva3_6.xlsx')
        main()
    elif choice==5:
        start=time.perf_counter()*1000
        pr=list(brute_force(alphabet,3,4))
        end=time.perf_counter()*1000
        print(pr)
        print('Time in ms:', end-start)
        df=pd.DataFrame(pr)
        df.to_excel('resva3_7.xlsx')
        main()
    elif choice==0: return 0
    else:
        print("Enter the number in range 0-5")
        main()

main()
