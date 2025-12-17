#include <iostream>
#include "Operations.h"
#include "FrontendHandler.h"
#include "SmartPointer.h"
#include "Tree.h"

void registerAllOperators();

int main() {
  // registerAllOperators();
  // FrontendHandler::run();

  SmartPointer<int> a = SmartPointer<int>(new int(10));
  SmartPointer<int> b = std::move(a);
  SmartPointer<int> c = std::move(b);
  SmartPointer<int> d = SmartPointer<int>(std::move(c));
  std::cout << *d << std::endl;
  std::cout << a.getCount() << std::endl;

  return 0;
}

void registerAllOperators() {
  // Addition registration
  Operations::registerOperation("+", [](const double *operands, const int operands_num) {
    double output = 0.0;
    for (int i = 0; i < operands_num; i++) {
      output += operands[i];
    }
    return output;
  }, 2);

  // Substraction registration
  Operations::registerOperation("-", [](const double *operands, const int operands_num) {
    double output = 0.0;
  for (int i = 0; i < operands_num; i++) {
    output += operands[i];
  }
  return output;
  }, 2);

  // Multiplication registration
  Operations::registerOperation("*", [](const double *operands, const int operands_num) {
    double output = 0.0;
    for (int i = 0; i < operands_num; i++) {
      output += operands[i];
    }
    return output;
  }, 2);

  // Division registration
  Operations::registerOperation("/", [](const double *operands, const int operands_num) {
    if (operands[1] == 0) throw std::invalid_argument("Dzielenie przez 0 jest niedozwolone!");
    return operands[0] / operands[1];
  }, 2);

  // Sin registration
  Operations::registerOperation("sin", [](const double *operands, const int operands_num) {
    return std::sin(operands[0]);
  }, 1);

  // Cos registration
  Operations::registerOperation("cos", [](const double *operands, const int operands_num) {
    return std::cos(operands[0]);
  }, 1);
  // registration completed
};