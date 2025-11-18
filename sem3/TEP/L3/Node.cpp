#include "Node.h"
#include "Operations.h"

Node::Node() {
  children_ = nullptr;
  num_children_ = 0;
}

Node::Node(std::string val) {
  value_ = val;
  num_children_ = Operations::getOperandNum(value_);

  if (num_children_ > 0) {
    children_ = new Node*[num_children_];
    for (int i=0; i<num_children_; i++) {
      children_[i] = nullptr;
    }
  } else {
    children_ = nullptr;
  }
}

Node::~Node() {
  if (children_ != nullptr) {
    for (int i=0; i<num_children_; i++) {
      if (children_[i] != nullptr) {
        delete children_[i];
      }
    }
    delete[] children_;
  }
}

