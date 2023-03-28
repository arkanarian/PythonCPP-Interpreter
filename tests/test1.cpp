#include <typeinfo>
#include <iostream>
using namespace std;

//int df = 5; // declaration: записывается в список, первым записывается создание переменной, далее записывается присваивание значения

int main() {
//  const char* b_2 = "b";

  int main = 6 + 2;
  int main = 6 + 2; // само слово main не зарезервировано и может использоваться если main была функцией а это переменная
  char a = 'a', r = '3';
  char b = 'a';
  char include = 'a'; // само слово include не зарезервировано
  const char* bc = "bc"; // отлавливается строка
  char ac = 'a'; // invalid, only last char assigning
  char endl = "\n"; // endl может быть и числом и любым символом
//  const char* d = bc + b_; // invalid
  char c = a + b * (4-2*(-5)); // непонятный момент
  cout << a << endl;
  cout << 3+2*5 << 2 << endl; // ФИЧА: не отлавливается как битовый сдвиг
  int dtg = 3 << 2 * 5 + -4 << 4; // ФИЧА: отлавливается как битовый сдвиг
  int dtg = 2 * 5 << 3 << 76; // ФИЧА: отлавливается как битовый сдвиг
  int dtg = 3 + 4 + 5 + 6; // ФИЧА: отлавливается как битовый сдвиг
  cout << dtg << endl;
  cout << include << endl;
  cout << b << endl;
  cout << include << endl;
  cout << bc << endl;
  cout << "c = " << int(c) << endl;
  cout << "c = " << (int)c << endl;
  cout << c << endl;
  cout << df << endl;
  cout << main << endl;
  cout << b_2 << endl;
//  return 0;
}

int df2 = 5;