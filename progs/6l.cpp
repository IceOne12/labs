#include <iostream>
#include <cmath>

using namespace std;

extern "C"
{
    void _6lab_as();
    double x;
    double result;
}

void main(){
    result = 0.0;
    cout<<'Введите x:'<<endl;
    cin>>x;
    _6lab_as();
    cout<<result<<endl;

    system("pause");

}