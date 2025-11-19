#ifndef L3_FRONTENDHANDLER_H
#define L3_FRONTENDHANDLER_H
#include <string>
#include "Tree.h"

class FrontendHandler {
public:
  FrontendHandler() = delete;
  static void run();
private:
  static Tree* tree_;
  static void handleEnter(std::string args);
  static void handlePrint();
  static void handleVars();
  static void handleComp(std::string args);
  static void handleJoin(std::string args);
};

#endif //L3_FRONTENDHANDLER_H