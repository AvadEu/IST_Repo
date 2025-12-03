#pragma once
#include <map>
#include <string>
#include <sstream>
#include "Result.h"
#include "Error.h"

#include "Node.h"
class Tree;

using customResult = Result<Tree, Error>;

#ifndef L3_TREE_H
#define L3_TREE_H

class Tree {
public:
  Tree();
  ~Tree();

  Tree(const Tree &other);
  Tree &operator=(const Tree &other);
  void enter(const std::string& formula);
  customResult enterRes(const std::string& formula);
  static customResult createFromFormula(const std::string& formula);
  static customResult createAndThrow(const std::string& formula);
  Result<Tree*, Error> getTree(std::stringstream &formula);
  void join(Tree &tree);
  double compute(std::map<std::string, double> &vars);
  void print();
  void optimize();
  std::string getVars();
  void loadVars(Node* node, std::string *vars);
  std::string toString();
private:
  Node* root_;
  Node* parse(std::stringstream& ss);
  void print_helper(const Node* node);
  bool parse_warning_;
  bool parse_extra_;
  std::string extra_tokens_;
  void deconstruct(const Node* node);
  bool findReplaceLeaf(const Node* currentNode, Node* replacement);
  void getVarsHelper(Node* node, std::map<std::string, bool>& uniqueVars);
  double computeHelper(const Node* node, const std::map<std::string,double>& vars);
  bool allChildrenNumbers(const Node* node);
  std::string toString_helper(const Node* node);
  static customResult createTreeFromFormula(const std::string& formula);
};

#endif //L3_TREE_H