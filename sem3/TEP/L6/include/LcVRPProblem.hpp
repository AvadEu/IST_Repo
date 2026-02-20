#pragma once
#include "Problem.hpp"
#include "LcVRP_Evaluator.hpp"
#include "ProblemData.hpp"
#include <string>

class LcVRPProblem : public Problem {
public:
  LcVRPProblem(const std::string& folderPath, const std::string& fileName, int numGroups);
  ~LcVRPProblem();

  double Evaluate(const std::vector<int>& solution) override;
  int GetDimension() const override;
  int GetLowerBound() const override;
  int GetUpperBound() const override;

private:
  LcVRPContest::ProblemData* data_;
  LcVRPContest::LcVRP_Evaluator* evaluator_;
};