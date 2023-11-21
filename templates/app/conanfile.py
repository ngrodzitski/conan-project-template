from conans import ConanFile, CMake, tools
import os, sys, re

#%if "corporate_tag" in self.keys()
class @{corporate_tag.lower().capitalize()}@{camel_name}Conan(ConanFile):
#%else
class @{camel_name}Conan(ConanFile):
#%end if

    def set_version(self):
        version_file_path = os.path.join(
            self.recipe_folder,
            "@{name}/include/@{src_path_prefix}@{name}/version.hpp"
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

#%if "corporate_tag" in self.keys()
    name = "@{corporate_tag.lower()}@{name}"
#%else
    name = "@{name}"
#%end if

    license = "TODO"
    author = "TODO"
    url = "TODO"
    homepage = "TODO"
    description = "@{name} application"
    topics = ("@{name}", "todo")

    generators = "cmake_find_package", "cmake"
    settings = "os", "compiler", "build_type", "arch"

    no_copy_source = True
    build_policy = "missing"
    _cmake = None

    def build_requirements(self):
        # TODO: add your libraries here
        self.build_requires("fmt/[~10]")
        self.build_requires("gtest/1.14.0")

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake

        self._cmake = CMake(self)
        self._cmake.definitions["@{PROJECT_CMAKE_VAR_SUFFIX}_INSTALL"] = True
        self._cmake.definitions["@{PROJECT_CMAKE_VAR_SUFFIX}_CONAN_BUILD"] = True
        self._cmake.definitions[
            "@{PROJECT_CMAKE_VAR_SUFFIX}_BUILD_TESTS"
        ] = True

        self._cmake.configure()
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))
