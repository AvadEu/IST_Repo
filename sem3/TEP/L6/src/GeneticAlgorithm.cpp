#include "GeneticAlgorithm.hpp"
#include <iostream>
#include <limits>
#include <algorithm>

GeneticAlgorithm::GeneticAlgorithm(const AGParams &params)
    : params_(params), problem_(nullptr), rng_(std::random_device{}()) {
}

void GeneticAlgorithm::SetProblem(Problem* problem) {
    problem_ = problem;
    bestSolution_.fitness = std::numeric_limits<double>::max();
}

std::pair<std::vector<int>, double> GeneticAlgorithm::GetBestResult() const {
    return { bestSolution_.genotype, bestSolution_.fitness };
}

void GeneticAlgorithm::Run() {
    if(!problem_) return;

    Initialize();
    
    for(int i=0; i<params_.iterations; ++i) {
        Selection();
        Crossover();
        Mutation();
        EvaluateAll();
        
        if(i % 100 == 0) {
            std::cout << "Iteracja: " << i << " | Najlepszy wynik: " << bestSolution_.fitness << "\n";
        }
    }
}


GeneticAlgorithm::Individual GeneticAlgorithm::CreateRandomInd() {
    Individual ind;
    const int size = problem_->GetDimension();
    const int minVal = problem_->GetLowerBound();
    const int maxVal = problem_->GetUpperBound();
    
    ind.genotype.resize(size);
    std::uniform_int_distribution<int> dist(minVal, maxVal);
    
    for(int& gene : ind.genotype) gene = dist(rng_);
    return ind;
}

void GeneticAlgorithm::Initialize() {
    population_.clear();
    for(int i=0; i<params_.popSize; ++i) population_.push_back(CreateRandomInd());
    EvaluateAll();
}

void GeneticAlgorithm::EvaluateAll() {
    for(auto& ind : population_) {
        ind.fitness = problem_->Evaluate(ind.genotype);
        
        if(ind.fitness > 0 && ind.fitness < bestSolution_.fitness) {
            bestSolution_ = ind;
        }
    }
}

void GeneticAlgorithm::Selection() {
    std::vector<Individual> newPop;
    std::uniform_int_distribution<int> dist(0, population_.size() - 1);

    while(newPop.size() < population_.size()) {
        const int i1 = dist(rng_);
        const int i2 = dist(rng_);
        const double f1 = (population_[i1].fitness < 0) ? 1e9 : population_[i1].fitness;
        double f2 = (population_[i2].fitness < 0) ? 1e9 : population_[i2].fitness;

        if(f1 < f2) newPop.push_back(population_[i1]);
        else newPop.push_back(population_[i2]);
    }
    population_ = newPop;
}

void GeneticAlgorithm::Crossover() {
    std::uniform_real_distribution<double> dist(0.0, 1.0);
    std::uniform_int_distribution<int> pointDist(0, problem_->GetDimension() - 1);

    for (size_t i = 0; i < population_.size() - 1; i += 2) {
        if (dist(rng_) < params_.crossProb) {
            int point = pointDist(rng_);
            for (int j = point; j < problem_->GetDimension(); j++) {
                std::swap(population_[i].genotype[j], population_[i+1].genotype[j]);
            }
        }
    }
}

void GeneticAlgorithm::Mutation() {
    std::uniform_real_distribution<double> probDist(0.0, 1.0);
    std::uniform_int_distribution<int> valDist(problem_->GetLowerBound(), problem_->GetUpperBound());

    for (auto& ind : population_) {
        for (int& gene : ind.genotype) {
            if (probDist(rng_) < params_.mutProb) {
                gene = valDist(rng_);
            }
        }
    }
}