#include "Error.h"

Error::Error(const std::string &msg) {
  msg_ = msg;
}

std::string Error::getMsg() {
  return msg_;
}