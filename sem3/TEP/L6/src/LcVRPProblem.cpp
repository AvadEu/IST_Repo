#include "LcVRPProblem.hpp"
#include "ProblemLoader.hpp"

using namespace LcVRPContest;

LcVRPProblem::LcVRPProblem(const std::string& folderPath, const std::string& fileName, int numGroups) {
  ProblemLoader loader(folderPath, fileName);
  data_ = new ProblemData(loader.LoadProblem());
  evaluator_ = new LcVRP_Evaluator(*data_, numGroups);
}

LcVRPProblem::~LcVRPProblem() {
  delete evaluator_;
  delete data_;
}

double LcVRPProblem::Evaluate(const std::vector<int>& solution) {
  return evaluator_->Evaluate(solution);
}

int LcVRPProblem::GetDimension() const {
  return evaluator_->GetSolutionSize();
}

int LcVRPProblem::GetLowerBound() const {
  return evaluator_->GetLowerBound();
}

int LcVRPProblem::GetUpperBound() const {
  return evaluator_->GetUpperBound();
}