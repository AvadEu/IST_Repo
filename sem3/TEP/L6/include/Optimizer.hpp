#pragma once
#include "Problem.hpp"
#include <vector>
#include <utility>
#include <string>

class Optimizer {
public:
	virtual ~Optimizer() = default;
	virtual void SetProblem(Problem* problem) = 0;
	virtual void Run() = 0;
	virtual std::pair<std::vector<int>, double> GetBestResult() const = 0;
	virtual std::string GetName() const = 0;
};