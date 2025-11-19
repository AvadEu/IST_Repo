#include "FrontendHandler.h"
#include <iostream>
#include <sstream>
#include <list>
#include <map>

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
    } else if (command == "vars") {
      handleVars();
    } else if (command == "print") {
      handlePrint();
    } else if (command == "comp") {
      handleComp(args);
    } else if (command == "join") {
      handleJoin(args);
    } else if (command == "exit" || command == "quit") {
      return;
    } else {
      std::cout << "Unknown command: " << command << std::endl;
    }
  }
}

void FrontendHandler::handleEnter(std::string args) {
  tree_->enter(args);
  std::cout << "Drzewo zbudowane." << std::endl;
}

void FrontendHandler::handlePrint() {
  tree_->print();
}

void FrontendHandler::handleVars() {
  std::string vars = tree_->getVars();
  if (vars.empty()) {
    std::cout << "Brak zmiennych w drzewie." << std::endl;
  } else {
    std::cout << "Zmienne: " << vars << std::endl;
  }
}

void FrontendHandler::handleComp(std::string args) {
  std::string varsLine = tree_->getVars();

  std::stringstream vss(varsLine);
  std::stringstream s(args);
  std::string var;
  double value;
  std::map<std::string,double> valMap;
  size_t assigned = 0;

  if (!(vss >> var)) {
    std::stringstream s2(args);
    if (s2 >> value) {
      std::cout << "Warning: Drzewo nie zawiera zmiennych ignorowanie wartosci." << std::endl;
    }
    try {
      std::map<std::string,double> emptyMap;
      double result = tree_->compute(emptyMap);
      std::cout << "Wynik: " << result << std::endl;
    } catch (const std::exception &e) {
      std::cerr << "Blad wyliczania " << e.what() << std::endl;
    }
    return;
  }

  // there is at least one variable (we already read first into 'var')
  do {
    if (!(s >> value)) {
      // not enough values provided
      // count assigned so far is 'assigned'
      std::cout << "Ostrzezenie: liczba podanych wartosci (" << assigned << ") nie odpowiada liczbie zmiennych" << std::endl;
      return;
    }
    valMap[var] = value;
    ++assigned;
  } while (vss >> var);

  // check for extra provided values
  if (s >> value) {
    std::cout << "Ostrzezenie: podano wiecej wartosci niz liczba zmiennych; nadmiar zostanie zignorowany." << std::endl;
  }

  try {
    double result = tree_->compute(valMap);
    std::cout << "Wynik: " << result << std::endl;
  } catch (const std::exception &e) {
    std::cout << "Blad podczas obliczania: " << e.what() << std::endl;
  }
}
//
void FrontendHandler::handleJoin(std::string args) {
  Tree otherTree;
  otherTree.enter(args);

  tree_->join(otherTree);
  std::cout << "Drzewa polaczone." << std::endl;
}
