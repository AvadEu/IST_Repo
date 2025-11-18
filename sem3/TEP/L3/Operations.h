#pragma once
#include <map>
#include <functional>

#ifndef L3_OPERATIONS_H
#define L3_OPERATIONS_H

class Operations {
public:
    using Operation = std::function<double(double *operands, int operands_num)>;

    Operations() = delete;
    Operations(const Operations&) = delete;
    Operations& operator=(const Operations&) = delete;
    ~Operations() = delete;
    static void registerOperation(const std::string& name, const Operation& op, int operand_num);
    static double execute(const std::string& name, double *operands, int operands_num);
    static int getOperandNum(const std::string& name);
private:
    static std::map<std::string, Operation> operations_;
    static std::map<std::string, int> operand_num_;
};

#endif //L3_OPERATIONS_H