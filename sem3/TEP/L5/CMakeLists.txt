cmake_minimum_required(VERSION 4.0)
project(L5)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED On)

include_directories(include)

set(SOURCES
    src/main.cpp
    src/RefCounter.cpp
    src/RefCounter.cpp
    include/SmartPointer.h
    src/Node.cpp
    src/Operations.cpp
    src/FrontendHandler.cpp
    src/Tree.cpp
)

add_executable(L5 ${SOURCES})
