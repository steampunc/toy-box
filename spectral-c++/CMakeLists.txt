cmake_minimum_required(VERSION 3.15)
project(spectral_c)

set(CMAKE_CXX_STANDARD 14)

add_library(matplotlibcpp matplotlibcpp.h)
add_executable(spectral_c main.cpp utils.cpp)
target_link_libraries(spectral_c fftw3)
add_subdirectory(gtest)

