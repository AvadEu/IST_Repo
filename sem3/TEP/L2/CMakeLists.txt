cmake_minimum_required(VERSION 4.0)
project(L2)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED On)

add_executable(L2 main.cpp
        Number.cpp
        Number.h)
