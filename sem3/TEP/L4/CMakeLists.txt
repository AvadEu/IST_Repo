cmake_minimum_required(VERSION 4.0)
project(L4)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED On)

#set(HEADERS
#    Node.h
#    Tree.h
#    Operations.h
#    FrontendHandler.h
#)

set(SOURCES
    src/Node.cpp
    src/Tree.cpp
    src/main.cpp
    src/Operations.cpp
    src/FrontendHandler.cpp
        include/Result.h
        src/Error.cpp
        include/FileWriter.h
)

add_executable(L4 ${SOURCES} ${HEADERS})

target_include_directories(L4 PUBLIC ${PROJECT_SOURCE_DIR}/include)
