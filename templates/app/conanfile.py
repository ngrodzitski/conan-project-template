from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import rmdir
from conan.tools.scm import Version
import os, sys, re

#%if "corporate_tag_camel" in self.keys()
class @{corporate_tag_camel}@{camel_name}Conan(ConanFile):
#%else
class @{camel_name}Conan(ConanFile):
#%end if

    def set_version(self):
        version_file_path = os.path.join(
            self.recipe_folder,
            "@{styled_name}/include/@{src_path_prefix}@{styled_name}/version.hpp"
        )
        with open(version_file_path, 'r') as file:
            content = file.read()
            major_match = re.search(r'VERSION_MAJOR\s+(\d+)ull', content)
            minor_match = re.search(r'VERSION_MINOR\s+(\d+)ull', content)
            patch_match = re.search(r'VERSION_PATCH\s+(\d+)ull', content)

            if major_match and minor_match and patch_match:
                major = int(major_match.group(1))
                minor = int(minor_match.group(1))
                patch = int(patch_match.group(1))
                self.version = f"{major}.{minor}.{patch}"
            else:
                raise ValueError(f"cannot detect version from {version_file_path}")

#%if "corporate_tag_normalized_word" in self.keys()
    name = "@{corporate_tag_normalized_word.lower()}_@{styled_name}"
#%else
    name = "@{styled_name}"
#%end if

    license = "TODO"
    author = "TODO"
    url = "TODO"
    homepage = "TODO"
    description = "@{styled_name} application"
    topics = ("@{styled_name}", "todo")

    settings = "os", "compiler", "build_type", "arch"

    no_copy_source = True
    build_policy = "missing"
    _cmake = None

    def requirements(self):
        # TODO: add your libraries here
        self.requires("fmt/[~10]")

    def build_requirements(self):
        # TODO: add your libraries here
        self.test_requires("gtest/1.14.0")

    def layout(self):
        cmake_layout(self, src_folder=".", build_folder=".")
        self.folders.generators = ""

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["@{PROJECT_CMAKE_VAR_SUFFIX}_INSTALL"] = True
        tc.variables["@{PROJECT_CMAKE_VAR_SUFFIX}_CONAN_BUILD"] = True
        tc.variables[
            "@{PROJECT_CMAKE_VAR_SUFFIX}_BUILD_TESTS"
        ] = True

        tc.generate()

        cmake_deps = CMakeDeps(self)
        cmake_deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder=self.source_folder)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
