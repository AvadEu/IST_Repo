#include "FrontendHandler.h"
#include <iostream>
#include <sstream>

const std::string WELCOME_MESSAGE = "Witaj w programie do przetwarzania wyrażeń przy pomocy drzew!\n";
const std::string COMMAND_PROMPT_INDICATOR = "> ";

Tree* FrontendHandler::tree_ = new Tree();

void FrontendHandler::run() {

  std::string prompt, command;

  std::cout << WELCOME_MESSAGE;

  while (true) {
    std::cout << COMMAND_PROMPT_INDICATOR;

    std::getline(std::cin, prompt);
    if (prompt.empty()) continue;

    std::stringstream ss(prompt);
    ss >> command;

    std::string args;
    std::getline(ss, args);

    if (command == "enter") {
      handleEnter(args);
    // } else if (command == "vars") {
    //   handleVars();
    } else if (command == "print") {
      handlePrint();
    // } else if (command == "comp") {
    //   handleComp(args);
    // } else if (command == "join") {
    //   handleJoin(args);
    } else if (command == "exit" || command == "quit") {
      return;
    } else {
      std::cout << "Unknown command: " << command << std::endl;
    }
  }
}

void FrontendHandler::handleEnter(std::string args) {
  // args zawiera np. " + * 5 sin x" (ze spacją na początku)
  tree_->enter(args);
  std::cout << "Drzewo zbudowane." << std::endl;
}

void FrontendHandler::handlePrint() {
  tree_->print();
}

// void FrontendHandler::handleVars() {
//   std::vector<std::string> vars = tree_.getVars();
//   std::cout << "Zmienne: ";
//   for (size_t i = 0; i < vars.size(); i++) {
//     std::cout << vars[i] << " ";
//   }
//   std::cout << std::endl;
// }
//
// void FrontendHandler::handleComp(std::string args) {
//   // args ma postać: " x 5 y 3"
//   std::stringstream ss(args);
//   std::string name;
//   double val;
//   std::map<std::string, double> valMap;
//
//   // Parsujemy pary: zmienna wartość
//   while (ss >> name >> val) {
//     valMap[name] = val;
//   }
//
//   double result = tree_.compute(valMap);
//   std::cout << "Wynik: " << result << std::endl;
// }
//
// void FrontendHandler::handleJoin(std::string args) {
//   // args to formuła drugiego drzewa
//   Tree otherTree;
//   otherTree.enter(args);
//
//   tree_.join(otherTree);
//   std::cout << "Drzewa polaczone." << std::endl;
// }
