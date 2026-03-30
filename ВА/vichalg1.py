import sys
import pandas as pd
import time
def buble(mas):
    swap=True
    while swap:
        swap=False
        for i in range(len(mas)-1):
            if mas[i]>mas[i+1]:
                mas[i],mas[i+1]=mas[i+1],mas[i]
                swap=True
                
def merge(left_list,right_list):
    sorted_list=[]
    left_list_index = right_list_index = 0
    left_list_length, right_list_length = len(left_list),len(right_list)
    for _ in range(left_list_length + right_list_length):
        if left_list_index < left_list_length and right_list_index< right_list_length:
            if left_list[left_list_index]<=right_list[right_list_index]:
                sorted_list.append(left_list[left_list_index])
                left_list_index +=1
            else:
                sorted_list.append(right_list[right_list_index])
                right_list_index +=1
        elif left_list_index == left_list_length:
            sorted_list.append(right_list[right_list_index])
            right_list_index +=1
        elif right_list_index == right_list_length:
            sorted_list.append(left_list[left_list_index])
            left_list_index +=1

    
    return sorted_list
def merge_sort(num):
    if len(num) <=1:
        return num
    mid= len(num)//2
    left_list = merge_sort(num[:mid])
    right_list = merge_sort(num[mid:])

    return merge(left_list, right_list)
def main():
    print("Введите 1-4 для выбора задания, 0 для выхода")
    print("1.Buble sort")
    print("2.Merge sort")
    print("3.Include in python sort")
    print("0.Exit")
    choice=int(input())
    if choice==1:   
        mas=[118,118,110,114,94,99,119,101,116,116,117,118,118,119,115,111,99,110,110,111,104,120,110,114,99,118,98,101,116,116,105,120,120,116,119,104,113,111,99,100,116,118,113,101,105,118,118,109,118,109,109,116,99,114,113]
        start=time.perf_counter()*1000
        buble(mas)
        end=time.perf_counter()*1000
        print("Buble sort", mas,"Time:", end-start,'ms')
        df=pd.DataFrame(mas)
        df.to_excel('mas1.xlsx')
        main()
    if choice==2:
        mas=[118,118,110,114,94,99,119,101,116,116,117,118,118,119,115,111,99,110,110,111,104,120,110,114,99,118,98,101,116,116,105,120,120,116,119,104,113,111,99,100,116,118,113,101,105,118,118,109,118,109,109,116,99,114,113]
        start=time.perf_counter()*1000
        mas=merge_sort(mas)
        end=time.perf_counter()*1000
        print("Merge",mas,"Time:",end-start,"ms")
        df=pd.DataFrame(mas)
        df.to_excel('mas_.xlsx')
        main()

    if choice==3:
        mas=[118,118,110,114,94,99,119,101,116,116,117,118,118,119,115,111,99,110,110,111,104,120,110,114,99,118,98,101,116,116,105,120,120,116,119,104,113,111,99,100,116,118,113,101,105,118,118,109,118,109,109,116,99,114,113]
        start=time.perf_counter()*1000
        mas.sort()
        end= time.perf_counter()*1000
        print("Include sort", mas, "Time:", end-start,"ms")
        df=pd.DataFrame(mas)
        df.to_excel('mas.xlsx')
        main()
    if choice==0:
        return 0
        
    
    else:
        print("Введите 0-4!")
        main()
main()
