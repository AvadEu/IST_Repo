#include <iostream>
#include "Number.h"
#include <functional>

std::ostream operator<<(const std::ostream & lhs, const Number & rhs);

int main() {
  // std::cout << "Hello, World!" << std::endl;
  // Number* n = new Number(123);
  // *n = 1234;
  // *n = -5001;
  // *n = Number(1520);
  // std::cout << (Number(-24) * Number(-5)).toString() << "\n";
  std::cout << (Number(732) << 2U) << std::endl;
  std::cout << (Number(732) << Number(1)) << std::endl;
  std::cout << Number(30);
  std::function<int(int)> myFunc = [] (const int x ) {
    return x * 2;
  };
  return 0;
}
