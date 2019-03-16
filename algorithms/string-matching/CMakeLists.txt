cmake_minimum_required(VERSION 2.6)
project(Strings)
add_compile_options(-std=c++17 -g)

add_executable(bruteforce brute-force.cpp)
add_executable(kmp kmp.cpp)
