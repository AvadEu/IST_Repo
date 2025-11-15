cmake_minimum_required(VERSION 4.0)
project(L1_mod)

set(CMAKE_CXX_STANDARD 98)

set(SOURCES
        main.cpp
        Student.cpp
        Course.cpp
)

set(HEADERS
        Course.h
        Student.h
)

add_executable(main ${SOURCES} ${HEADERS})