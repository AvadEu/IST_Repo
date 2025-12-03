#ifndef L4_MOD_MAPPER_H
#define L4_MOD_MAPPER_H
#include <vector>

template<class Funct>
class Mapper {
  public:
  Mapper() = default;
  ~Mapper() = default;

  void operator()(std::vector<typename Funct::ValueType> &vector) {
    for (int i = 0; i < vector.size(); i++) {
      vector[i] = Funct()(vector[i]);
    }
  }
};


#endif //L4_MOD_MAPPER_H