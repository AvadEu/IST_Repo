cmake_minimum_required(VERSION 4.0)
project(L1)

set(CMAKE_CXX_STANDARD 98)

set(SOURCES
    main.cpp
    solution.cpp
        Table.cpp
)

set(HEADERS
    solution.h
        Table.h
)

add_executable(main ${SOURCES} ${HEADERS})