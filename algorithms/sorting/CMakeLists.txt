cmake_minimum_required(VERSION 3.0.0)
project(Sorting VERSION 0.1.0)
add_compile_options(-std=c++17)

add_executable(bubblesort bubble.cpp)
add_executable(heapsort heapsort.cpp)
add_executable(insertsort insertion.cpp)
add_executable(mergesort merge.cpp)
add_executable(quicksort quicksort.cpp)
