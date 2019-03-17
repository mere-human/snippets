cmake_minimum_required(VERSION 3.0.0)
project(Strings VERSION 0.1.0)
add_compile_options(-std=c++17 -g)

add_executable(bruteforce brute-force.cpp)
add_executable(kmp kmp.cpp)
