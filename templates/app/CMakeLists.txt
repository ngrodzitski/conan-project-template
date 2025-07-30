# Root CMake for @{styled_name} project.
cmake_minimum_required(VERSION 3.21)

project(@{names.cmake_project_name} CXX)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# ------------------------------------------------------------------------------
# Various helpers:
include("${CMAKE_CURRENT_SOURCE_DIR}/cmake-scripts/common_options.cmake")

set(COMPILER_ENABLE_UNUSED_X_AS_ERROR OFF)
include("${CMAKE_CURRENT_SOURCE_DIR}/cmake-scripts/compiler_flags.cmake")

include( "${CMAKE_CURRENT_SOURCE_DIR}/cmake-scripts/find_program_required.cmake")
include( "${CMAKE_CURRENT_SOURCE_DIR}/cmake-scripts/static_analysis.cmake" )
include( "${CMAKE_CURRENT_SOURCE_DIR}/cmake-scripts/code_coverage.cmake" )

# ------------------------------------------------------------------------------
# Build options
option(@{names.cmake_var_suffix_upper}_INSTALL           "Generate install target"  ON)
option(@{names.cmake_var_suffix_upper}_BUILD_TESTS       "Build tests"              ON)
option(@{names.cmake_var_suffix_upper}_GCC_CODE_COVERAGE "Build with code coverage" OFF)
# ------------------------------------------------------------------------------

message(STATUS "@{names.cmake_var_suffix_upper}_INSTAL:            ${@{names.cmake_var_suffix_upper}_INSTALL}")
message(STATUS "@{names.cmake_var_suffix_upper}_BUILD_TEST:        ${@{names.cmake_var_suffix_upper}_BUILD_TESTS}")
message(STATUS "@{names.cmake_var_suffix_upper}_GCC_CODE_COVERAGE: ${@{names.cmake_var_suffix_upper}_GCC_CODE_COVERAGE}")

set(CMAKE_FIND_PACKAGE_PREFER_CONFIG ON)

# TODO: Add conan-provided libraries here:
find_package(fmt REQUIRED)

#%if @qml
# TODO: Adjust version and components as necessary
find_package(Qt6 6.8 REQUIRED COMPONENTS Core Gui Qml Quick)
message(STATUS "Qt6_FOUND=${Qt6_FOUND}")
message(STATUS "Qt6_DIR=${Qt6_DIR}")

#%end if
if (@{names.cmake_var_suffix_upper}_GCC_CODE_COVERAGE)
    make_code_coverage_targets(
        NAME CodeCoverage
        HTML_TITLE "Code coverage report for @styled_name app"
        FILTERS
            '${CMAKE_SOURCE_DIR}/@{names.styled_name}/src/.*'
            '${CMAKE_SOURCE_DIR}/@{names.styled_name}/include/.*'
    )
endif()

# ===================================
add_subdirectory(@{names.styled_name})

if (@{names.cmake_var_suffix_upper}_BUILD_TESTS)
    include(CTest)
    enable_testing()
    message(STATUS "Tests are enabled")

    find_package(GTest MODULE REQUIRED)

    add_subdirectory(@{names.styled_name}/test)
endif ()
