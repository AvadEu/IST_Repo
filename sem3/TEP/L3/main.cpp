#include <iostream>
#include "Operations.h"


void registerAllOperators();

int main() {
  registerAllOperators();
  std::cout << "Hello, World!" << std::endl;
  double *operands = new double[3];
  operands[0] = 3.0;
  operands[1] = 4.0;
  operands[2] = 5.0;
  std::cout << Operations::execute("sin", operands, 1) << std::endl;
  delete[] operands;
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
  Operations::registerOperation("sin", [](const double *operands, const int operands_num) {
    return std::cos(operands[0]);
  }, 1);
};