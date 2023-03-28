include <typeinfo>
#include <iostream>
using namespace std;

// some comment
/* multiline comment
is ended here */

int main() {

// loop to access each array element
  for (int step = 0; step < size; ++step) {

    // loop to compare array elements
    for (int i = 0; i < size - step; ++i) {

      // compare two adjacent elements
      // change > to < to sort in descending order
//      if (array[i] > array[i + 1]) {

        // swapping elements if elements
        // are not in the intended order
//        int temp = array[i];
//        array[i] = array[i + 1];
//        array[i + 1] = temp;
      }
    }
  }
  for (int i = 0; i < size; ++i) {
//    cout << "  " << array[i];
  }
  cout << "\n";

  int data = {-2, 45, 0, 11, -9};

  // find array's length
  int size = sizeof(data) / sizeof(data0);

  bubbleSort(data, size);

  cout << "Sorted Array in Ascending Order:\n";
  printArray(data, size);

}

int df2 = 5;
