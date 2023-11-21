cmake_minimum_required(VERSION 3.14)

# Define where cmake-scripts dir is located.
# in case of using this lib as a submodule it might be located somewhere else
# and not next to a root `CMakeLists.txt` file of the project.
if (NOT @{PROJECT_CMAKE_VAR_SUFFIX}_CMAKE_SCRIPTS_DIR)
    # If not explicitly set use a default one:
    set(@{PROJECT_CMAKE_VAR_SUFFIX}_CMAKE_SCRIPTS_DIR "${CMAKE_SOURCE_DIR}/cmake-scripts")
endif ()

# ====================================================================
# Version
# ====================================================================
include(${@{PROJECT_CMAKE_VAR_SUFFIX}_CMAKE_SCRIPTS_DIR}/extract_version.cmake)
extract_version(
    "include/@{src_path_prefix}${@{PROJECT_CMAKE_VAR_SUFFIX}_APPLICATION_NAME}/version.hpp"
    # Define extracted version as following:
    PRJ_VERSION_MAJOR
    PRJ_VERSION_MINOR
    PRJ_VERSION_PATCH
)

set(PRJ_VERSION ${PRJ_VERSION_MAJOR}.${PRJ_VERSION_MINOR}.${PRJ_VERSION_PATCH})
message(STATUS "${@{PROJECT_CMAKE_VAR_SUFFIX}_APPLICATION_NAME} VERSION  : " ${PRJ_VERSION})

# ====================================================================
# Declare project
# ====================================================================
#%if @project_cmake_var_suffix == @name
set(TARGET_PROJECT ${@{PROJECT_CMAKE_VAR_SUFFIX}_APPLICATION_NAME})
#%else
set(TARGET_PROJECT @{project_cmake_var_suffix}${@{PROJECT_CMAKE_VAR_SUFFIX}_APPLICATION_NAME})
#%end if

project(${TARGET_PROJECT} LANGUAGES CXX VERSION ${PRJ_VERSION})

# ====================================================================
# Set sources
# ====================================================================
list(APPEND  target_headers
    include/@{src_path_prefix}${@{PROJECT_CMAKE_VAR_SUFFIX}_APPLICATION_NAME}/version.hpp
    include/@{src_path_prefix}${@{PROJECT_CMAKE_VAR_SUFFIX}_APPLICATION_NAME}/main.hpp
    # TODO: your header files.
)

list(APPEND target_src
    src/@{src_path_prefix}${@{PROJECT_CMAKE_VAR_SUFFIX}_APPLICATION_NAME}/main.cpp
    # TODO: your src files.
)

# ====================================================================
# TARGET
# ====================================================================

# Define essential applications routine as library.
# This will allow us to use it in tests, thus we can do testing
# the same way as with libraries.
add_library(${TARGET_PROJECT}_lib STATIC ${target_headers} ${target_src})
add_library(${TARGET_PROJECT}::${TARGET_PROJECT}_lib ALIAS ${TARGET_PROJECT}_lib)

set(PROJECT_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/include)
message(STATUS "${TARGET_PROJECT}_lib include dir: ${PROJECT_INCLUDE_DIR}")
target_include_directories(${TARGET_PROJECT}_lib PUBLIC ${PROJECT_INCLUDE_DIR})

target_link_libraries(${TARGET_PROJECT}_lib PUBLIC
    # TODO: set your dependencies
    fmt::fmt
)

# A final executable:
add_executable(${TARGET_PROJECT} src/main.cpp)
target_link_libraries(${TARGET_PROJECT} ${TARGET_PROJECT}::${TARGET_PROJECT}_lib)

# Targets for install
list(APPEND TARGETS_LIST ${TARGET_PROJECT})
# ====================================================================

# ====================================================================
# Install
# ====================================================================
if (@{PROJECT_CMAKE_VAR_SUFFIX}_INSTALL)
    include(GNUInstallDirs)
    include(CMakePackageConfigHelpers)

    install(TARGETS ${TARGETS_LIST}
        EXPORT ${TARGET_PROJECT}_project_targets
    )
endif ()
