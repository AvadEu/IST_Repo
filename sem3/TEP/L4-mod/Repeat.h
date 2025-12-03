//
// Created by Wiktor Golimowski on 03/12/2025.
//

#ifndef L4_MOD_REPEAT_H
#define L4_MOD_REPEAT_H

template<typename T, unsigned N>
class Repeat {
public:
  typedef T ValueType;

  Repeat() = default;
  ~Repeat() = default;

  ValueType operator()(const ValueType &op) {
    ValueType outcome = T();
    for (int i = 0; i < N; i++) {
      outcome += op;
    }
    return outcome;
  }
};

#endif //L4_MOD_REPEAT_H