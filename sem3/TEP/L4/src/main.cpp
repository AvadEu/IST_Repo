#include <iostream>
#include <cmath>
#include "Operations.h"
#include "FrontendHandler.h"
#include "Error.h"
#include <Result.h>
#include "Tree.h"
#include "FileWriter.h"


void registerAllOperators();

int main() {
  registerAllOperators();

  Result<Tree, Error> res = Tree::createFromFormula(" + 1");
  if (res.isSuccess()) {
    res.getValue().print();
  } else {
    std::vector<Error*> errs = res.getErrors();
    for (const auto & err : errs) {
      std::string msg = err->getMsg();
      std::cout << msg << std::endl;
    }
  }

  FileWriter::vSaveToFile(res, "outcome.txt");
  // FrontendHandler::run();
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