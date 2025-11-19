cmake_minimum_required(VERSION 4.0)
project(L3)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED On)

set(HEADERS
    Node.h
    Tree.h
    Operations.h
    FrontendHandler.h
)

set(SOURCES
    Node.cpp
    Tree.cpp
    main.cpp
    Operations.cpp
    FrontendHandler.cpp
)

add_executable(L3 ${SOURCES} ${HEADERS})
