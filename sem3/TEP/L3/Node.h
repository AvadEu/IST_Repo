#ifndef L3_NODE_H
#define L3_NODE_H
#include <string>

class Node {
public:
  Node();
  explicit Node(std::string val);
  ~Node();
private:
  std::string value_;
  Node** children_;
  int num_children_;
};


#endif //L3_NODE_H