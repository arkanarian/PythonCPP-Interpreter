// числовые и текстовы константы
1, 2.5, 'c'

// 3-4 типа переменных
int a; // без задания значения
int a = 5;
char a = 'a';
float a = 5.0;
double a = 5.0;
bool a = true

// do..while, for
do {
  i++;
  cout << i;
}
while (i < 5)

for (int i = 0; i < 5; i++){
  cout << i;
}

while (i<5){
  i++;
  cout << i;
}
// if..else, switch
if (i == 0){
  cout << i;
} else if (i == 1){
  cout << i;
} else {
  cout << i;
}

int b = 3;
int a = 3;
switch (a){
  case 1:
    cout << "1";
    break;
  case 2:
    cout << "2";
    break;
  case b:
    cout << "3";
    break; // если нет break дальше идти
  default:
    cout << "def";
    break;
}

//Rules for naming a variable
//
// A variable name can only have alphabets, numbers, and the underscore _.
// A variable name cannot begin with a number.
// It is a preferred practice to begin variable names with a lowercase character. For example, name is preferable to Name.
// A variable name cannot be a keyword. For example, int is a keyword that is used to denote integers.
// A variable name can start with an underscore. However, it's not considered a good practice.


//// Char ////
char ch = 'h';
char ch = ''' // error
char ch = ' \'' // no error
// reserved character
// \b - backspace
// \f - form feed
// \n - newline
// \r - return
// \t - horiz tab
// \v - vertical tab
// \\ - backslash
// \' - single quote
// \" - double quote
// \? - question mark
// \0 - null


//// Float ////
float a = -2.0
float a = 0.0000234
float a = -0.22E-5
double a = 45E12    // 45E12 is equal to 45*10^12


//// Modifiers ////
signed
unsigned
short
long

//// C-strings ////
char str[] = "C++";
char str[4] = "C++";
char str[3] = "C++"; // raises error
char str[4] = {'C','+','+','\0'};
char str[100];
cin >> str; // читает всю строку


//// Const ///
const int LIGHT_SPEED = 299792458;
LIGHT_SPEED = 2500 // Error! LIGHT_SPEED is a constant.
#define LIGHT_SPEED 299792458;

//// Output ////
#include <iostream>
using namespace std;

int main() {
    // prints the string enclosed in double quotes
    int a = 5;
    cout << "This is C++ Programming";
    cout << "This is C++ Programming" << a << endl;
    return 0;
}

//// Input ////
#include <iostream>
using namespace std;

cin >> num;
cin >> num >> a; // multiple inputs


//// Type Conversion ////
float b = 5.4;
int a = int(b); // 5