#include <iostream>
#include <cmath>
#include <iomanip>

using namespace std;

cout<< fixed << setprecision(15) << endl;

extern "C"
{
    void l6();
    void l62();
    float x;
    float result=0.0;
    float y=0.0;
}

double func(double x){
    double result;
    if(x<0){result=cos(x)*cos(x);}
    else if(x>0.5){result= tan(x)*tan(x);}
    else{result=pow(2,x)+3;}
    return result;
}
double calc(double x) {
    // sqrt(x^4 - 1)
    double sqrt_val = sqrt(x * x * x * x - 1);
    
    // log2(sqrt(x^4 - 1))
    double log_val = log2(sqrt_val);

    // 2 * sin(x) * log2(sqrt(x^4 - 1)) + 1
    double numerator = 2 * sin(x) * log_val + 1;

    // (2 * sin(x) + pi/6) / (2 * pi)
    double denominator = 6.2831853072 /(sin(2*x) + 0.5235987756) ;

    // arctg^2(log2(sqrt(x^4 - 1)))
    double atan_squared = atan(log_val) * atan(log_val);

    // Финальный результат
    result = numerator / denominator - atan_squared ;
    return result;
}
void main(){
    double y = 0.0
    cout<<"Vasilev V.V. IUK2-33B"<<endl
    double result = 0.0;
    cout << "if x<0 --> y=cos^2x \nif 0<=x<=0.5 --> y=2^x +3\nif x>0.5 --> y=tg^2x\nВведите x:" ;
    while (cin >> x) {
        if ((x <= 1) && (x >= -1)) {
            cout << "invalid x, enter again"<<endl;
            cout << "Enter x : ";
        }
        else { break; }
    }
   
    cout << endl;
    cout<<"\n\n\n\nTask 1"<<endl;
    result=calc(x);
    cout<<"(c++) b= ";
    cout<<result<<endl;
    cout<<"(asm) b= ";
    l6();
    cout<<result<<endl;
    cout<<"\n\n\n\nTask 2"<<endl;
    y=func(x);
    cout<<"(c++) y= ";
    cout<<y<<endl;
    l62();
    cout<<"(asm) y= ";
    count<<y<<endl;
    return 0;

}