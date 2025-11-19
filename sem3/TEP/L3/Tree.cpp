#include "Tree.h"

#include <iostream>

Tree::Tree() {
  root_ = nullptr;
}

Tree::~Tree() {
  deconstruct(root_);
}

Tree::Tree(const Tree &other) {
  if (other.root_ != nullptr) {
    root_ =  new Node(*other.root_);
  } else {
    root_ = nullptr;
  }
}

Tree& Tree::operator=(const Tree& other) {
  if (this != &other) {
    deconstruct(root_);
    if (other.root_) {
      root_ = new Node(*other.root_);
    } else {
      root_ = nullptr;
    }
  }
  return *this;
}

void Tree::deconstruct(const Node* node) {
    delete node;
}

void Tree::enter(const std::string& formula) {
  deconstruct(root_);
  std::stringstream ss(formula);
  root_ = parse(ss);
}

Node* Tree::parse(std::stringstream& ss) {
  std::string token;

  if (!(ss >> token)) {
    return new Node("1");
  }

  Node* node = new Node(token);

  for (int i = 0; i < node->getChildCount(); i++) {
    Node* child = parse(ss);
    node->setChild(i, child);
  }

  return node;
}

void Tree::print() {
  if (root_) {
    std::cout << "Drzewo jest puste!" << std::endl;
  }
  print_helper(root_);
  std::cout << std::endl;
}

void Tree::print_helper(const Node* node) {
  if (!node) return;

  std::cout << node->getValue() << " ";

  for (int i = 0; i < node->getChildCount(); i++) {
    print_helper(node->getChild(i));
  }
}