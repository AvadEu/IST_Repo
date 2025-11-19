#ifndef L3_NODE_H
#define L3_NODE_H
#include <string>

class Node {
public:
  Node();
  explicit Node(std::string val);
  ~Node();
  Node(const Node& other);
  Node& operator=(const Node& other);
  int getChildCount() const;
  void setChild(int idx, Node* newChild) const;
  std::string getValue() const;
  Node* getChild(int idx) const;
private:
  std::string value_;
  Node** children_;
  int num_children_;
  Node* deepCopy(const Node* other);
};


#endif //L3_NODE_H