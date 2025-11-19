#include "Operations.h"

std::map<std::string, Operations::Operation> Operations::operations_;
std::map<std::string, int> Operations::operand_num_;

void Operations::registerOperation(const std::string& name, const Operation& op, int operand_num) {
  operations_.emplace(name, op);
  operand_num_.emplace(name, operand_num);
}

double Operations::execute(const std::string& name, double *operands, const int operands_num) {
  return operations_.at(name)(operands, operands_num);
}

int Operations::getOperandNum(const std::string& name) {
  std::map<std::string, int>::iterator it = operand_num_.find(name);
  if (it == operand_num_.end()) {
    return 0;
  }
  return it->second;
}

bool Operations::isNumber(const std::string& str) {
  if (str.empty()) {
    return false;
  }
  char *endptr = nullptr;
  std::strtod(str.c_str(), &endptr);
  return (*endptr == '\0');
}