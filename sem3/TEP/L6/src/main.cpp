#include <iostream>
#include <string>
#include "LcVRPProblem.hpp"
#include "GeneticAlgorithm.hpp"


int main() {
    Problem* problem = nullptr;
    Optimizer* optimizer = nullptr;

    std::cout << "=== OPTIMIZATION FRAMEWORK ===\n";

    std::string folderPath, fileName;
    std::cout << "Podaj nazwe zestawu (np. Vrp-Set-A): ";
    std::cin >> folderPath;
    std::cout << "Podaj nazwe pliku (np. A-n32-k5): ";
    cin >> fileName;

    std::cout << "Wczytywanie problemu: " << fileName << " z " << folderPath + "/" + fileName << "...\n";
    problem = new LcVRPProblem(folderPath, fileName, 21);

    std::cout << "Konfiguracja Algorytmu Genetycznego...\n";
    AGParams params(100, 0.05, 0.6, 2000);
    optimizer = new GeneticAlgorithm(params);

    optimizer->SetProblem(problem);

    std::cout << "Start obliczen...\n";
    optimizer->Run();

    std::pair<std::vector<int>, double> result = optimizer->GetBestResult();
    std::cout << "\n=== WYNIKI KONCOWE ===\n";
    std::cout << "Metoda: " << optimizer->GetName() << "\n";
    std::string outcome;
    for (const int elem: result.first) {
        outcome += std::to_string(elem);
    }
    std::cout << "Genotyp: " << outcome << "\n";
    std::cout << "Koszt:  " << result.second << "\n";

    delete optimizer;
    delete problem;
    optimizer = nullptr;
    problem = nullptr;

    delete optimizer;
    delete problem;

    return 0;
}