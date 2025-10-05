cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES CXX)

macro(test_llvm_cmake_variable VARIABLE)
    if(NOT DEFINED ${VARIABLE})
        message(FATAL_ERROR "${VARIABLE} is not defined")
    endif()
    message(STATUS "${VARIABLE}: ${${VARIABLE}}")
endmacro()

set(CMAKE_CXX_STANDARD 17)
add_executable(${PROJECT_NAME} test_package.cpp)

if (CLANG_SHARED)
    find_package(Clang REQUIRED)
    target_link_libraries(${PROJECT_NAME} PRIVATE Clang)
else()
    find_package(Clang REQUIRED)
    target_link_libraries(${PROJECT_NAME} PRIVATE clangBasic)
endif()

message(STATUS "Testing Clang Build Module Variables")
test_llvm_cmake_variable(CLANG_CMAKE_DIR)
