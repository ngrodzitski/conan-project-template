cmake_minimum_required(VERSION 3.14)

if (NOT @{PROJECT_CMAKE_VAR_SUFFIX}_LIBRARY_NAME)
    set(@{PROJECT_CMAKE_VAR_SUFFIX}_LIBRARY_NAME @{name})
endif ()

# ====================================================================
# Version
# ====================================================================

# Define where cmake-scripts dir is located.
# in case of using this lib as a submodule it might be located somewhere else
# and not next to a root `CMakeLists.txt` file of the project.
if (NOT @{PROJECT_CMAKE_VAR_SUFFIX}_CMAKE_SCRIPTS_DIR)
    # If not explicitly set use a default one:
    set(@{PROJECT_CMAKE_VAR_SUFFIX}_CMAKE_SCRIPTS_DIR "${CMAKE_SOURCE_DIR}/cmake-scripts")
endif ()

include(${@{PROJECT_CMAKE_VAR_SUFFIX}_CMAKE_SCRIPTS_DIR}/extract_version.cmake)
extract_version(
    "include/@{src_path_prefix}${@{PROJECT_CMAKE_VAR_SUFFIX}_LIBRARY_NAME}/version.hpp"
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

message(STATUS "${@{PROJECT_CMAKE_VAR_SUFFIX}_LIBRARY_NAME} VERSION  : " ${PRJ_VERSION})
message(STATUS "${@{PROJECT_CMAKE_VAR_SUFFIX}_LIBRARY_NAME} SOVERSION: " ${PRJ_SOVERSION})

# ====================================================================
# Declare project
# ====================================================================

#%if @project_cmake_var_suffix == @name
set(TARGET_PROJECT ${@{PROJECT_CMAKE_VAR_SUFFIX}_LIBRARY_NAME})
#%else
set(TARGET_PROJECT @{project_cmake_var_suffix}${@{PROJECT_CMAKE_VAR_SUFFIX}_LIBRARY_NAME})
#%end if

project(${TARGET_PROJECT} LANGUAGES CXX VERSION ${PRJ_VERSION})

# ====================================================================
# Set sources
# ====================================================================

list(APPEND TARGET_PUBLIC_HEADERS
    include/@{src_path_prefix}${@{PROJECT_CMAKE_VAR_SUFFIX}_LIBRARY_NAME}/pub.hpp
    include/@{src_path_prefix}${@{PROJECT_CMAKE_VAR_SUFFIX}_LIBRARY_NAME}/version.hpp
)

#%if not @header_only
list(APPEND  target_private_headers
    include/@{src_path_prefix}${@{PROJECT_CMAKE_VAR_SUFFIX}_LIBRARY_NAME}/impl/helpers.hpp
)

list(APPEND target_src
    src/@{src_path_prefix}${@{PROJECT_CMAKE_VAR_SUFFIX}_LIBRARY_NAME}/pub.cpp
    src/@{src_path_prefix}${@{PROJECT_CMAKE_VAR_SUFFIX}_LIBRARY_NAME}/impl/helpers.cpp
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
add_library(${TARGET_PROJECT}::${TARGET_PROJECT} ALIAS ${TARGET_PROJECT})
add_library(${TARGET_PROJECT}::${@{PROJECT_CMAKE_VAR_SUFFIX}_LIBRARY_NAME} ALIAS ${TARGET_PROJECT})

set(PROJECT_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/include)
message("${TARGET_PROJECT} include_dir: ${PROJECT_INCLUDE_DIR}")

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
                           @{library_macros}
)

# Targets for install
list(APPEND TARGETS_LIST ${TARGET_PROJECT})
# ====================================================================

# ====================================================================
# Install
# ====================================================================
if (@{PROJECT_CMAKE_VAR_SUFFIX}_INSTALL)
    include(${@{PROJECT_CMAKE_VAR_SUFFIX}_CMAKE_SCRIPTS_DIR}/lib_install.cmake)

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
