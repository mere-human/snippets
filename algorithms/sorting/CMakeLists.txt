cmake_minimum_required(VERSION 2.6)
project(Sorting)
add_compile_options(-std=c++17)

add_executable(bubblesort bubble.cpp)
add_executable(heapsort heapsort.cpp)
add_executable(insertsort insertion.cpp)
add_executable(mergesort merge.cpp)
add_executable(quicksort quicksort.cpp)
