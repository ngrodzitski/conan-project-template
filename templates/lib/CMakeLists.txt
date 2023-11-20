# Root CMake for @{name} project.
cmake_minimum_required(VERSION 3.15)

set(@{PROJECT_CMAKE_VAR_SUFFIX}_LIBRARY_NAME @{name})

#%if @project_cmake_var_suffix == @name
project(${@{PROJECT_CMAKE_VAR_SUFFIX}_LIBRARY_NAME}_root CXX)
#%else
project(@{project_cmake_var_suffix}_${@{PROJECT_CMAKE_VAR_SUFFIX}_LIBRARY_NAME}_root CXX)
#%end if

option(@{PROJECT_CMAKE_VAR_SUFFIX}_CONAN_BUILD
    "A flag that tells if this is a conan controlled build" OFF)

include("${CMAKE_CURRENT_SOURCE_DIR}/cmake-scripts/cpp_standard.cmake")

if (@{PROJECT_CMAKE_VAR_SUFFIX}_CONAN_BUILD)
    # Using conan "cmake" generator for packaging.
    # https://docs.conan.io/en/latest/integrations/build_system/cmake/cmake_generator.html#cmake-generator
    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup(TARGETS)

else ()
    include("${CMAKE_CURRENT_SOURCE_DIR}/cmake-scripts/libcxx.cmake")
    include( "${CMAKE_CURRENT_SOURCE_DIR}/cmake-scripts/static_runtime.cmake" )

    if ("${@{PROJECT_CMAKE_VAR_SUFFIX}_CPPSTD}" STREQUAL "20" )
        message(STATUS "ENABLE C++20")
        cxx_20()
    else ()
        message(STATUS "ENABLE C++17")
        cxx_17()
    endif ()

    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

    # ------------------------------------------------------------------------------
    # Assume using conan "cmake_find_package" generator.
    # https://docs.conan.io/en/latest/integrations/build_system/cmake/cmake_find_package_generator.html
    list(APPEND CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR})
    # ------------------------------------------------------------------------------

    handle_explicit_libcxx_if_necessary()
    handle_explicit_static_runtime_if_necessary()

    # ------------------------------------------------------------------------------
    # Various helpers:
    include("${CMAKE_CURRENT_SOURCE_DIR}/cmake-scripts/common_options.cmake")

    set(COMPILER_ENABLE_UNUSED_X_AS_ERROR OFF)
    include("${CMAKE_CURRENT_SOURCE_DIR}/cmake-scripts/compiler_flags.cmake")

    include("${CMAKE_CURRENT_SOURCE_DIR}/cmake-scripts/find_program_required.cmake")
    include( "${CMAKE_CURRENT_SOURCE_DIR}/cmake-scripts/static_analysis.cmake" )
    include( "${CMAKE_CURRENT_SOURCE_DIR}/cmake-scripts/code_coverage.cmake" )
endif ()

# ------------------------------------------------------------------------------
# Build options
option(@{PROJECT_CMAKE_VAR_SUFFIX}_INSTALL           "Generate install target"  ON)
option(@{PROJECT_CMAKE_VAR_SUFFIX}_BUILD_TESTS       "Build tests"              ON)
option(@{PROJECT_CMAKE_VAR_SUFFIX}_GCC_CODE_COVERAGE "Build with code coverage" OFF)
# ------------------------------------------------------------------------------

message(STATUS "@{PROJECT_CMAKE_VAR_SUFFIX}_INSTAL:            ${@{PROJECT_CMAKE_VAR_SUFFIX}_INSTALL}")
message(STATUS "@{PROJECT_CMAKE_VAR_SUFFIX}_BUILD_TEST:        ${@{PROJECT_CMAKE_VAR_SUFFIX}_BUILD_TESTS}")
message(STATUS "@{PROJECT_CMAKE_VAR_SUFFIX}_GCC_CODE_COVERAGE: ${@{PROJECT_CMAKE_VAR_SUFFIX}_GCC_CODE_COVERAGE}")

# TODO: Add conan-provided libraries here:
find_package(fmt REQUIRED)

if (@{PROJECT_CMAKE_VAR_SUFFIX}_GCC_CODE_COVERAGE)
    make_code_coverage_targets(
        NAME CodeCoverage
        HTML_TITLE "Code coverage report for @name library"
        FILTERS
            '${CMAKE_SOURCE_DIR}/${@{PROJECT_CMAKE_VAR_SUFFIX}_LIBRARY_NAME}/src/.*'
            '${CMAKE_SOURCE_DIR}/${@{PROJECT_CMAKE_VAR_SUFFIX}_LIBRARY_NAME}/include/.*'
    )
endif()

# ===================================
add_subdirectory(${@{PROJECT_CMAKE_VAR_SUFFIX}_LIBRARY_NAME})

if (@{PROJECT_CMAKE_VAR_SUFFIX}_BUILD_TESTS)
    include(CTest)
    enable_testing()
    message(STATUS "Tests are enabled")

    set(CMAKE_FIND_PACKAGE_PREFER_CONFIG ON)
    find_package(GTest MODULE REQUIRED)

    add_subdirectory(${@{PROJECT_CMAKE_VAR_SUFFIX}_LIBRARY_NAME}/test)
endif ()
