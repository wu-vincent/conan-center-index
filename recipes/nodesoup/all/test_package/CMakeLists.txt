cmake_minimum_required(VERSION 3.15)
project(test_package CXX)

find_package(nodesoup REQUIRED CONFIG)

add_executable(${CMAKE_PROJECT_NAME} test_package.cpp)
target_link_libraries(${CMAKE_PROJECT_NAME} nodesoup::nodesoup)
set_property(TARGET ${CMAKE_PROJECT_NAME} PROPERTY CXX_STANDARD 17)
