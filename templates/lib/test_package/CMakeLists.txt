cmake_minimum_required(VERSION 3.8)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

#%if "corporate_tag" in self.keys()
#%set @ctag=@corporate_tag.lower()
#%else
#%set @ctag=""
#%end if
find_package(@{ctag}@{name} REQUIRED)

add_executable(example example.cpp)
target_link_libraries(example @{ctag}@{name}::@{name})
