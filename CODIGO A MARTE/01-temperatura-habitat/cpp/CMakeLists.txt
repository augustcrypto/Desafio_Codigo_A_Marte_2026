cmake_minimum_required(VERSION 3.15)
project(ControlTemperaturaMarciano VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Opciones de compilación para sistemas críticos
if(MSVC)
    add_compile_options(/W4 /WX /O2)
else()
    add_compile_options(-Wall -Wextra -Wpedantic -Werror -O3)
endif()

# Encontrar threads (necesario para std::thread)
find_package(Threads REQUIRED)

# Ejecutable principal
add_executable(control_temperatura control_temperatura.cpp)

# Enlazar con threads
target_link_libraries(control_temperatura PRIVATE Threads::Threads)

# Propiedades adicionales
set_target_properties(control_temperatura PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
)