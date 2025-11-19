#pragma once
#include <map>
#include <string>
#include <sstream>

#include "Node.h"

#ifndef L3_TREE_H
#define L3_TREE_H

class Tree {
public:
  Tree();
  ~Tree();

  Tree(const Tree &other);
  Tree &operator=(const Tree &other);
  void enter(const std::string& formula);
  void join(Tree &tree);
  double compute(std::map<std::string, double> &vars);
  void print();

  std::string *getVars();
  void loadVars(Node* node, std::string *vars);
private:
  Node* root_;
  static Node* parse(std::stringstream& ss);
  void print_helper(const Node* node);
  void deconstruct(const Node* node);

};

#endif //L3_TREE_H