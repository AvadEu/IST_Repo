#pragma once
#include <string>

#ifndef L4_ERROR_H
#define L4_ERROR_H

class Error {
public:
  Error() = default;
  explicit Error(const std::string &msg);
  ~Error() = default;
  std::string getMsg();
private:
  std::string msg_;
};

#endif //L4_ERROR_H
