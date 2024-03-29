set(test_prj _utest.${@{PROJECT_CMAKE_VAR_SUFFIX}_LIBRARY_NAME})

project(${test_prj})

list(APPEND  unittests_srcfiles
    #TODO: adjust as necessary
     pub.cpp
#%if not @header_only
     impl/helpers.cpp
#%end if
     )

add_executable(${test_prj} ${unittests_srcfiles})

if (WIN32)
    target_compile_definitions(${test_prj} PRIVATE _CRT_SECURE_NO_WARNINGS)
endif ()

target_link_libraries(${test_prj}
                      PRIVATE
                      GTest::gtest_main
#%if @project_cmake_var_suffix == @name
                      @{name}::@{name}
#%else
                      @{project_cmake_var_suffix}_@{name}::@{name}
#%end if
)

include(GoogleTest)

# Distinguishing tests for CI ([Debug, Release, ...] x [devtoolset, other gcc, clang],,,)
# If the variable is defined test report would also include this tag
# as a part of the test name.
gtest_discover_tests(${test_prj}
                     TEST_PREFIX "${@{PROJECT_CMAKE_VAR_SUFFIX}_TEST_PREFIX}")
