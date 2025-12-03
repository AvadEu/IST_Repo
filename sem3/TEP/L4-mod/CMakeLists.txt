cmake_minimum_required(VERSION 4.0)
project(L4_mod)

set(CMAKE_CXX_STANDARD 11)

add_executable(L4_mod main.cpp
        Repeat.h
        Mapper.h)
