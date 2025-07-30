cmake_minimum_required(VERSION 3.21)

# Define where cmake-scripts dir is located.
# in case of using this lib as a submodule it might be located somewhere else
# and not next to a root `CMakeLists.txt` file of the project.
if (NOT @{names.cmake_var_suffix_upper}_CMAKE_SCRIPTS_DIR)
    # If not explicitly set use a default location (in the root dir):
    set(@{names.cmake_var_suffix_upper}_CMAKE_SCRIPTS_DIR "${CMAKE_SOURCE_DIR}/cmake-scripts")
endif ()

# ====================================================================
# Version
# ====================================================================
include(${@{names.cmake_var_suffix_upper}_CMAKE_SCRIPTS_DIR}/extract_version.cmake)
extract_version(
    "include/@{names.src_path_prefix}/version.hpp"
    # Define extracted version as following:
    PRJ_VERSION_MAJOR
    PRJ_VERSION_MINOR
    PRJ_VERSION_PATCH
)

set(PRJ_VERSION ${PRJ_VERSION_MAJOR}.${PRJ_VERSION_MINOR}.${PRJ_VERSION_PATCH})
# ABI compatibility version.
# A safer approach is to declare compatibility on the level of minor version.
# If a major version compatibility is chosen then consider changing
# a COMPATIBILITY type in install section (SameMinorVersion => SameMajorVersion).
set(PRJ_SOVERSION ${PRJ_VERSION_MAJOR}.${PRJ_VERSION_MINOR})

message(STATUS "@{names.styled_name} VERSION  : " ${PRJ_VERSION})
message(STATUS "@{names.styled_name} SOVERSION: " ${PRJ_SOVERSION})

# ====================================================================
# Declare project
# ====================================================================

set(TARGET_PROJECT @{names.cmake_project_name})
project(${TARGET_PROJECT} LANGUAGES CXX VERSION ${PRJ_VERSION})

# ====================================================================
# Set sources
# ====================================================================

list(APPEND TARGET_PUBLIC_HEADERS
    include/@{names.src_path_prefix}/pub.hpp
    include/@{names.src_path_prefix}/version.hpp
)

#%if not @header_only
list(APPEND  target_private_headers
    include/@{names.src_path_prefix}/impl/helpers.hpp
)

list(APPEND target_src
    src/@{names.src_path_prefix}/pub.cpp
    src/@{names.src_path_prefix}/impl/helpers.cpp
)

#%end if
# ====================================================================
# TARGET
# ====================================================================
#%if @header_only
add_library(${TARGET_PROJECT} INTERFACE ${TARGET_PUBLIC_HEADERS})
#%else
add_library(${TARGET_PROJECT} STATIC ${TARGET_PUBLIC_HEADERS}
                                     ${target_private_headers}
                                     ${target_src}
)
#%end if
add_library(@{names.cmake_alias_target_name} ALIAS ${TARGET_PROJECT})

set(PROJECT_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/include)
message(STATUS "${TARGET_PROJECT} include_dir: ${PROJECT_INCLUDE_DIR}")

target_include_directories(${TARGET_PROJECT}
#%if @header_only
                           INTERFACE
#%else
                           PUBLIC
#%end if
                           $<BUILD_INTERFACE:${PROJECT_INCLUDE_DIR}>
                           $<INSTALL_INTERFACE:include>
)

# Set dependencies here:
target_link_libraries(${TARGET_PROJECT}
#%if @header_only
                      INTERFACE
#%else
                      PUBLIC
#%end if
                      #TODO: add dependencies here
                      fmt::fmt
)

target_compile_definitions(${TARGET_PROJECT}
#%if @header_only
                           INTERFACE
#%else
                           PUBLIC
#%end if
                           @{names.cpp_library_macros}
)

# Targets for install
list(APPEND TARGETS_LIST ${TARGET_PROJECT})
# ====================================================================

# ====================================================================
# Install
# ====================================================================
if (@{names.cmake_var_suffix_upper}_INSTALL)
    include(${@{names.cmake_var_suffix_upper}_CMAKE_SCRIPTS_DIR}/lib_install.cmake)

    lib_install(
        TARGET_PROJECT ${TARGET_PROJECT}
        VERSION "${PRJ_VERSION}"
        LIB_CONFIG cmake/lib-config.cmake.in
        TARGETS_LIST ${TARGETS_LIST}
    )

    lib_install_headers(
        REMOVE_INCLUDE_DIR_PREFIX include
        HEADERS ${TARGET_PUBLIC_HEADERS}
    )
endif ()
