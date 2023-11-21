set(test_prj _utest.${@{PROJECT_CMAKE_VAR_SUFFIX}_APPLICATION_NAME})

project(${test_prj})

list(APPEND  unittests_srcfiles
    #TODO: adjust as necessary
     sample_test.cpp
     )

add_executable(${test_prj} ${unittests_srcfiles})

if (WIN32)
    target_compile_definitions(${test_prj} PRIVATE _CRT_SECURE_NO_WARNINGS)
endif ()

target_link_libraries(${test_prj}
                      GTest::gtest_main
#%if @project_cmake_var_suffix == @name
                      @{name}::@{name}_lib
#%else
                      @{project_cmake_var_suffix}@{name}::@{project_cmake_var_suffix}@{name}_lib
#%end if
)

include(GoogleTest)

# Distingushisg tests for CI ([Debug, Release, ...] x [devtoolset, other gcc, clang],,,)
# If the variable is defined test report would also include this tag
# as a part of the test name.
gtest_discover_tests(${test_prj}
                     TEST_PREFIX "${@{PROJECT_CMAKE_VAR_SUFFIX}_TEST_PREFIX}")
