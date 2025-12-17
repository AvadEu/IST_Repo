#include "Tree.h"
#include "Operations.h"
#include <iostream>
#include <queue>

Tree::Tree() {
  root_ = nullptr;
  parse_warning_ = false;
  parse_extra_ = false;
  extra_tokens_.clear();
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

Tree::Tree(Tree&& other) noexcept {
  root_ = other.root_;
  parse_warning_ = other.parse_warning_;
  parse_extra_ = other.parse_extra_;
  extra_tokens_ = std::move(other.extra_tokens_);
  other.root_ = nullptr;
}

Tree Tree::operator=(const Tree& other) {
  if (this != &other) {
    deconstruct(root_);
    if (other.root_) {
      root_ = new Node(*other.root_);
    } else {
      root_ = nullptr;
    }
    parse_warning_ = other.parse_warning_;
    parse_extra_ = other.parse_extra_;
    extra_tokens_ = other.extra_tokens_;
  }
  return *this;
}

Tree Tree::operator=(Tree&& other) noexcept {
  if (this != &other) {
    deconstruct(root_);
    root_ = other.root_;
    parse_warning_ = other.parse_warning_;
    parse_extra_ = other.parse_extra_;
    extra_tokens_ = std::move(other.extra_tokens_);
    other.root_ = nullptr;
  }
  return *this;
}

Tree Tree::operator+(const Tree &other) const {
  Tree result(*this);
  Tree otherCopy(other);
  result.join(otherCopy);
  return result;
}

void Tree::deconstruct(const Node* node) {
    delete node;
}

void Tree::enter(const std::string& formula) {
  parse_warning_ = false;
  parse_extra_ = false;
  extra_tokens_.clear();

  deconstruct(root_);
  std::stringstream ss(formula);
  root_ = parse(ss);

  std::string leftover;
  if (ss >> leftover) {
    extra_tokens_ = leftover;
    std::string rest;
    while (ss >> rest) {
      extra_tokens_ += std::string(" ") + rest;
    }
    parse_extra_ = true;
  }

  if (parse_warning_) {
    std::cout << "Warning: Za mała liczba operandów. Przetwarzana będzie formuła: " << std::endl;
    print();
    parse_warning_ = false;
  }

  if (parse_extra_) {
    std::cout << "Warning: Za duża liczba operandów. Nadmiarowe tokeny zostaną pominięte. Nadmiar: " << extra_tokens_ << std::endl;
    print();
    parse_extra_ = false;
    extra_tokens_.clear();
  }
}

Node* Tree::parse(std::stringstream& ss) {
  std::string token;

  if (!(ss >> token)) {
    parse_warning_ = true;
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
  if (!root_) {
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

void Tree::join(Tree& otherTree) {
    if (!root_) {
        std::cerr << "Err: Nie mozna dolaczyc do pustego drzewa." << std::endl;
        return;
    }
    if (!otherTree.root_) {
        std::cerr << "Ostrzezenie: Drugie drzewo jest puste, operacja zignorowana." << std::endl;
        return;
    }

    Node* replacement = new Node(*otherTree.root_);

    if (!findReplaceLeaf(root_, replacement)) {
        std::cerr << "Err: Nie znaleziono liscia do podmiany." << std::endl;
        delete replacement;
    }
}


bool Tree::findReplaceLeaf(const Node* currentNode, Node* replacement) {
    if (!currentNode) return false;

    if (currentNode->getChildCount() == 0) {
        return false;
    }

    for (int i = 0; i < currentNode->getChildCount(); i++) {
        Node* child = currentNode->getChild(i);

        if (!child) continue;

        if (child->getChildCount() == 0) {

            currentNode->setChild(i, replacement);
            return true;
        }

        if (findReplaceLeaf(child, replacement)) {
            return true;
        }
    }

    return false;
}

void Tree::getVarsHelper(Node* node, std::map<std::string, bool>& uniqueVars) {
  if (!node) return;

  if (node->getChildCount() == 0 && !Operations::isNumber(node->getValue())) {

    uniqueVars[node->getValue()] = true;
  }

  for (int i = 0; i < node->getChildCount(); i++) {
    getVarsHelper(node->getChild(i), uniqueVars);
  }
}

double Tree::computeHelper(const Node* node, const std::map<std::string,double>& vars) {
  if (!node) throw std::invalid_argument("Err: brak zbudowanego drzewa");

  if (node->getChildCount() == 0) {
    std::string v = node->getValue();
    if (Operations::isNumber(v)) {
      return std::stod(v);
    }
    std::map<std::string,double>::const_iterator it = vars.find(v);
    if (it == vars.end()) {
      throw std::invalid_argument(std::string("Err: nieznana zmienna ") + v);
    }
    return it->second;
  }

  int n = node->getChildCount();
  double *ops = new double[n];
  for (int i = 0; i < n; ++i) {
    ops[i] = computeHelper(node->getChild(i), vars);
  }
  double res = Operations::execute(node->getValue(), ops, n);
  delete[] ops;
  return res;
}

double Tree::compute(std::map<std::string, double> &vars) {
  if (!root_) throw std::runtime_error("Drzewo jest puste");
  return computeHelper(root_, vars);
}


std::string Tree::getVars() {
  std::map<std::string, bool> uniqueVars;

  getVarsHelper(root_, uniqueVars);

  std::string result = "";

  std::map<std::string, bool>::iterator it = uniqueVars.begin();
  for (; it != uniqueVars.end(); ++it) {
    result += it->first;
    result += " ";
  }

  if (!result.empty() && result[result.length() - 1] == ' ') {
    result.erase(result.length() - 1);
  }

  return result;
}
void Tree::optimize() {
  if (!root_) return;

  std::queue <Node*> queue;
  queue.push(root_);

  while (!queue.empty()) {
    Node* node = queue.front();
    queue.pop();
    for (int i = 0; i < node->getChildCount(); i++) {
      Node* child = node->getChild(i);

      if (allChildrenNumbers(child)) {
        std::map<std::string, double> uniqueVars;
        double res = computeHelper(child, uniqueVars);
        std::cout << res << std::endl;
        Node* newNode = new Node(std::to_string(res));
        node->setChild(0, newNode);
      }
    }

    for (int i = 0; i < node->getChildCount(); i++) {
      Node* child = node->getChild(i);
      queue.push(child);
    }
  }
}


bool Tree::allChildrenNumbers(const Node *node) {
  if (!node) return false;
  if (node->getChildCount() == 0) return false;
  for (int i = 0; i < node->getChildCount(); i++) {
    if (!Operations::isNumber(node->getChild(i)->getValue())) return false;
  }
  return true;
}
