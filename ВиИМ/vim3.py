from scipy import integrate
from matplotlib import pyplot as plt
import numpy as np

print("Laboratory Work №3 Vasilev V.V.")
x1 = np.linspace(0,2,100)
def func(x1):
    y = (x1**4 + 5*x1**3-5**0.5*x1**2+3)**0.5
    return y

def equal_mesure(counts_n,cn_b):
    x0 = 0.3050692026
    n = counts_n
    mas2=[]
    mas2.append(x0)
    m=2**31-1
    a=48271
    al=0
    b=cn_b
    current_x=int(x0*m)
    for i in range(1,n):
        current_x=(a*current_x%m)
        norm_x=current_x/m
        mas2.append(norm_x)
    mas=[]
    for i in range(n):
        x_i=al+(b-al)*mas2[i]
        mas.append(x_i)
    return mas

def monte_carlo(b,a,mas):
    mult=(b-a)/len(mas)
    summ=0
    for i in range(1,len(mas)):
        summ+=mas[i]
    res=mult*summ
    return res

def monte_carlo2(b,a,M,mas_x,mas_y):
    mult=(b-a)*M
    Nbot=0
    for i in range(len(mas_x)):
        if mas_y[i]<mas_x[i]:
            Nbot+=1
    div=Nbot/len(mas_x)
    res=mult*div
    return res
    
result=func(x1)
plt.plot(x1,result)
plt.title("Grafics of function, 1 task\n max(f(x))=7.08")
plt.xlabel("Axis X")
plt.ylabel("Axis Y")
plt.grid(True)

plt.show()

result, _ = integrate.quad(func,0,2)
print("-"*50)
print('2.Square of curved trapezoid is',result)
mas=equal_mesure(100,2)
mas1=np.array(mas)
mas2=func(mas1)
res=monte_carlo(2,0,mas2)
e1=result-res
print('3. Method Monte-Carlo (1 way,n=100)\nSquare of curved trapezoid is', res,'\nError',e1)
mass=equal_mesure(1000,2)
mass1=np.array(mass)
mass2=func(mass1)
ress=monte_carlo(2,0,mass2)
e2=result-ress
print('4. Method Monte-Carlo (1 way,n=1000)\nSquare of curved trapezoid is', ress,'\nError',e2)
print('5. 1 way relationship error is',e1/e2)
masx=np.array(equal_mesure(100,2))
masy=np.array(equal_mesure(200,7.1))
masy=masy[100:]

masfx=func(masx)
masres=monte_carlo2(2,0,7.1,masfx,masy)
e3=result-masres
print('6. Method Monte-Carlo (2 way, n=100)\nSquare of curved trapezoid is',masres,'\nError',e3)
masx1=np.array(equal_mesure(1000,2))
masy1=np.array(equal_mesure(2000,7.1))
masy1=masy1[1000:]

masfx1=func(masx1)
masres1=monte_carlo2(2,0,7.1,masfx1,masy1)
e4=result-masres1
print('7. Method Monte-Carlo (2 way, n=1000)\nSquare of curved trapezoid is',masres1,'\nError',e4)
print('8. 2 way relationship error is ',e3/e4)

fig=plt.figure(figsize=[10,7])
ax = plt.axes(projection="3d")

ax.plot3D([0, 6], [0, 0], [0, 0], 'red', linewidth=2)
ax.plot3D([0, 0], [0, 10], [0, 0], 'red', linewidth=2)
ax.plot3D([0, 0], [0, 0], [0, 30], 'red', linewidth=2)
ax.plot3D([6, 0], [0, 10], [0, 0], 'red', linewidth=2)
ax.plot3D([6, 0], [0, 0], [0, 30], 'red', linewidth=2)
ax.plot3D([0, 0], [10, 0], [0, 30], 'red', linewidth=2)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
a=6
b=10
c=30
Vobj=1/6*a*b*c
V=a*b*c
ax.set_title('Task 9\nTetraedr: 5x + 3y + z = 30\n V=300')
plt.show()

print('10. Volume of a parallelepiped is', V)

masxi=equal_mesure(1000,6)
masyi=equal_mesure(2000,10)
maszi=equal_mesure(3000,30)
masyi=masyi[1000:]
maszi=maszi[2000:]
K=0
for i in range(len(masxi)):
    if 5*masxi[i]+3*masyi[i]+maszi[i]<=30:
        K+=1
Vobj_m_c=V*K/len(masxi)
e5=abs(Vobj-Vobj_m_c)
print('11. Monte-Carlo method (n=1000)\nVolume of a object is', Vobj_m_c,'\nError',e5)

masxi1=equal_mesure(10000,6)
masyi1=equal_mesure(20000,10)
maszi1=equal_mesure(30000,30)
masyi1=masyi1[10000:]
maszi1=maszi1[20000:]
K=0
for i in range(len(masxi1)):
    if 5*masxi1[i]+3*masyi1[i]+maszi1[i]<=30:
        K+=1
Vobj_c=V*K/len(masxi1)
e6=abs(Vobj-Vobj_c)
print('12. Monte-Carlo method (n=10000)\nVolume of a object is', Vobj_c,'\nError',e6)
print('13. Relationship error is' ,e5/e6)
print('-'*50)


'''
5x+3y+z=30
z=30-5x-3y ,z =0
30=5x+3y , x=0
30=3y
10=y (0,10,0), (0,0,0)
30=5x y=0
x=6 (6,0,0)
z=30 (0,0,30)'''

