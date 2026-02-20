#pragma once
#include "Optimizer.hpp"
#include <random>

struct AGParams {
  int popSize;
  double mutProb;
  double crossProb;
  int iterations;

  AGParams(const int p, const double m, const double c, const int i)
      : popSize(p), mutProb(m), crossProb(c), iterations(i) {}
};

class GeneticAlgorithm : public Optimizer {
public:
  GeneticAlgorithm(const AGParams &params);

  void SetProblem(Problem* problem) override;
  void Run() override;
  std::pair<std::vector<int>, double> GetBestResult() const override;
  std::string GetName() const override { return "Algorytm Genetyczny"; }

private:
  AGParams params_;
  Problem* problem_;

  struct Individual {
    std::vector<int> genotype;
    double fitness;
  };

  std::vector<Individual> population_;
  Individual bestSolution_;
  std::mt19937 rng_;

  void Initialize();
  void EvaluateAll();
  void Selection();
  void Crossover();
  void Mutation();
  Individual CreateRandomInd();
};