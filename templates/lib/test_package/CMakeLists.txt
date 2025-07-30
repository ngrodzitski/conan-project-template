cmake_minimum_required(VERSION 3.8)
project(test_package LANGUAGES CXX)

find_package(@{names.cmake_project_name} REQUIRED)

add_executable(${PROJECT_NAME} example.cpp)
target_link_libraries(${PROJECT_NAME} @{names.cmake_alias_target_name})
