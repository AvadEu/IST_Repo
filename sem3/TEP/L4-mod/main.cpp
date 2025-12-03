#include <iostream>
#include "Repeat.h"
#include "Mapper.h"

int main() {
  Mapper< Repeat<int, 5> > int_mapper;
  Mapper<Repeat<std::string, 2> > string_mapper;

  std::vector<int> vector = {1, 2, 3, 4, 5};
  std::vector<std::string> string_vector = {"abc", "foo"};

  int_mapper(vector);
  string_mapper(string_vector);

  for (int i = 0; i < vector.size(); i++) {
    std::cout << vector[i] << std::endl;
  }

  for (int i = 0; i < string_vector.size(); i++) {
    std::cout << string_vector[i] << std::endl;
  }
  return 0;
}