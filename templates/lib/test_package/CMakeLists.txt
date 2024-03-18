cmake_minimum_required(VERSION 3.8)
project(test_package LANGUAGES CXX)

#%if "corporate_tag_normalized_word" in self.keys()
#%set @ctag=@corporate_tag_normalized_word.lower() + "_"
#%else
#%set @ctag=""
#%end if
find_package(@{ctag}@{name} REQUIRED)

add_executable(${PROJECT_NAME} example.cpp)
target_link_libraries(${PROJECT_NAME} @{ctag}@{name}::@{name})
