#include "Operations.h"

std::map<std::string, Operations::Operation> Operations::operations_;
std::map<std::string, int> Operations::operand_num_;

void Operations::registerOperation(const std::string& name, const Operation& op, int operand_num) {
  operations_.emplace(name, op);
  operand_num_.emplace(name, operand_num);
}

double Operations::execute(const std::string& name, double *operands, const int operands_num) {
  if (operations_.count(name) == 0) {
    throw std::invalid_argument(std::string("Unknown operation: ") + name);
  }
  return operations_.at(name)(operands, operands_num);
}

int Operations::getOperandNum(const std::string& name) {
  if (operand_num_.count(name) == 0) {
    return 0;
  }
  return operand_num_.at(name);
}