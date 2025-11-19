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

Node::Node(const Node& other)
  : value_(other.value_),
    num_children_(other.num_children_) {
  if (num_children_ > 0) {
    children_ = new Node*[num_children_];
    for (int i=0; i<num_children_; i++) {
      children_[i] = deepCopy(other.children_[i]);
    }
  } else {
    children_ = nullptr;
  }
}

Node *Node::deepCopy(const Node *other) {
  if (!other) {
    return nullptr;
  } else {
    return new Node(*other);
  }
}

Node& Node::operator=(const Node& other) {
  if (this == &other) {
    return *this;
  }
  this->~Node();

  value_ = other.value_;
  num_children_ = other.num_children_;

  if (num_children_ > 0) {
    children_ = new Node*[num_children_];
    for (int i = 0; i < num_children_; i++) {
      children_[i] = deepCopy(other.children_[i]);
    }
  } else {
    children_ = nullptr;
  }

  return *this;
}

Node::~Node() {
  if (children_ != nullptr) {
    for (int i=0; i<num_children_; i++) {
      if (children_[i] != nullptr) {
        delete children_[i];
      }
    }
    delete[] children_;
    children_ = nullptr;
  }
}

int Node::getChildCount() const {
  return num_children_;
}

void Node::setChild(const int idx, Node* newChild) const {
  if (idx >= 0 && idx < num_children_) {
    if (children_[idx] != nullptr) {
      delete children_[idx];
    }
    children_[idx] = newChild;
  } else {
    throw std::out_of_range("Node::setChild: invalid index");
  }
}

std::string Node::getValue() const {
  return value_;
}

Node* Node::getChild(int idx) const {
  if (idx >= 0 && idx < num_children_) {
    return children_[idx];
  } else {
    throw std::out_of_range("Node::getChild: invalid index");
  }
}