cmake_minimum_required(VERSION 3.15)
project(ProteccionBitFlipsMarciano VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(MSVC)
    add_compile_options(/W4 /O2)
else()
    add_compile_options(-Wall -Wextra -O3)
endif()

add_executable(proteccion_bitflips proteccion_bitflips.cpp)

set_target_properties(proteccion_bitflips PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
)