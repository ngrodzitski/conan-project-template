import os

from conans import ConanFile, CMake, tools


#%if "corporate_tag" in self.keys()
#%set @ctag=@corporate_tag.lower()
#%else
#%set @ctag=""
#%end if
class @{ctag.capitalize()}@{camel_name}ConanTest(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "cmake_find_package"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self):
            bin_path = os.path.join("bin", "example")
            self.run(bin_path, run_environment=True)
