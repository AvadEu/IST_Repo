cmake_minimum_required(VERSION 4.1)
project(L6)

set(CMAKE_CXX_STANDARD 23)

include_directories(${CMAKE_SOURCE_DIR}/include)

set(SOURCES
    src/main.cpp
    src/LcVRP_Evaluator.cpp
    src/ProblemData.cpp
    src/ProblemLoader.cpp
    src/LcVRPProblem.cpp
    src/GeneticAlgorithm.cpp
)

add_executable(L6 ${SOURCES})
