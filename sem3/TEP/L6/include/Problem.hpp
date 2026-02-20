#pragma once
#include <vector>

class Problem {
public:
  virtual ~Problem() = default;

  virtual double Evaluate(const std::vector<int>& solution) = 0;

  virtual int GetDimension() const = 0;
  virtual int GetLowerBound() const = 0;
  virtual int GetUpperBound() const = 0;
};