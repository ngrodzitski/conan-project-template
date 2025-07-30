cmake_minimum_required(VERSION 3.21)

# Define where cmake-scripts dir is located.
# in case of using this lib as a submodule it might be located somewhere else
# and not next to a root `CMakeLists.txt` file of the project.
if (NOT @{names.cmake_var_suffix_upper}_CMAKE_SCRIPTS_DIR)
    # If not explicitly set use a default one:
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
message(STATUS "@{names.styled_name} VERSION  : " ${PRJ_VERSION})

# ====================================================================
# Declare project
# ====================================================================
set(TARGET_PROJECT @{names.cmake_project_name})

#%if @qml
qt_standard_project_setup(REQUIRES 6.7)
qt_policy(SET QTP0001 NEW)

#%end if
project(${TARGET_PROJECT} LANGUAGES CXX VERSION ${PRJ_VERSION})

# ====================================================================
# Set sources
# ====================================================================
list(APPEND  target_headers
    include/@{names.src_path_prefix}/version.hpp
    include/@{names.src_path_prefix}/main.hpp
    # TODO: your header files.
)

list(APPEND target_src
    src/@{names.src_path_prefix}/main.cpp
    # TODO: your src files.
)

# ====================================================================
# TARGET
# ====================================================================

# Define essential applications routine as library.
# This will allow us to use it in tests, thus we can do testing
# the same way as with libraries.
#%if @qml
qt_add_library(${TARGET_PROJECT}_lib STATIC ${target_headers} ${target_src})
#%else
add_library(${TARGET_PROJECT}_lib STATIC ${target_headers} ${target_src})
#%end if
add_library(@{names.cmake_alias_target_name}_lib ALIAS ${TARGET_PROJECT}_lib)

set_target_properties(
    ${TARGET_PROJECT}_lib PROPERTIES
    VERSION ${PRJ_VERSION}
    SOVERSION ${PRJ_VERSION_MAJOR}.${PRJ_VERSION_MINOR}
)

set(PROJECT_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/include)
message(STATUS "${TARGET_PROJECT}_lib include dir: ${PROJECT_INCLUDE_DIR}")
target_include_directories(${TARGET_PROJECT}_lib PUBLIC ${PROJECT_INCLUDE_DIR})

#%if @qml
# Remove entries (and related files) that are not needed.
qt_add_qml_module(${TARGET_PROJECT}_lib
    URI @{camel_name}
    VERSION 1.0
    QML_FILES
        # Custom Gui element.
        qml/MyButton.qml

        # Actual window to open.
        qml/MyMainWindow.qml
    RESOURCE_PREFIX "/"
    RESOURCES
        # Images:
        images/sample_image.png

        # JS:
        js/CommonUtils.js

        # Fonts:
        fonts/blocks-3x3-monospaced.ttf
    NO_PLUGIN
)
#%end if

#%if @qml
target_link_libraries(${TARGET_PROJECT}_lib PUBLIC
    # TODO: set your dependencies
    fmt::fmt

    Qt6::Core
    Qt6::Gui
    Qt6::Qml
    Qt6::Quick
    Qt6::QuickControls2
)

qt_import_qml_plugins(${TARGET_PROJECT}_lib)

qt_add_executable(${TARGET_PROJECT} src/main.cpp)
#%else
target_link_libraries(${TARGET_PROJECT}_lib PUBLIC
    # TODO: set your dependencies
    fmt::fmt
)

add_executable(${TARGET_PROJECT} src/main.cpp)
#%end if

# A final executable:
target_link_libraries(
    ${TARGET_PROJECT}
    PRIVATE
    @{names.cmake_alias_target_name}_lib
)

# Targets for install
list(APPEND TARGETS_LIST ${TARGET_PROJECT})
# ====================================================================

# ====================================================================
# Install
# ====================================================================
if (@{names.cmake_var_suffix_upper}_INSTALL)
    include(GNUInstallDirs)
    include(CMakePackageConfigHelpers)

    install(TARGETS ${TARGETS_LIST}
        EXPORT ${TARGET_PROJECT}_project_targets
    )
endif ()
