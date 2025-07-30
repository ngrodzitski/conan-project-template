from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import rmdir
from conan.tools.scm import Version
import os, sys, re


class @{names.conan_file_name}Conan(ConanFile):

    def set_version(self):
        version_file_path = os.path.join(
            self.recipe_folder,
            "@{names.styled_name}/include/@{names.src_path_prefix}/version.hpp"
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

#%if not @header_only
    options = {
        "fPIC": [True, False],
    }
    default_options = {
        "fPIC": True,
    }

#%end if
    name = "@{names.conan_package_name}"

    license = "TODO"
    author = "TODO"
    url = "TODO"
    homepage = "TODO"
    description = "@{names.styled_name} library"

    topics = ("@{names.styled_name}", "todo")

    settings = "os", "compiler", "build_type", "arch"

    exports_sources = [
        "CMakeLists.txt",
        "@{names.styled_name}/*",
        "cmake-scripts/*"
    ]
    no_copy_source = False
    build_policy = "missing"

    def _compiler_support_lut(self):
        return {
            "gcc": "9",
            "clang": "10",
            "apple-clang": "11",
            "Visual Studio": "17",
            "msvc": "191"
        }

    # This hint tells that this conanfile acts as
    # a conanfile for a package, which implies
    # it is responsible only for library itself.
    # Used to eliminate tests-related stuff (gtest, building tests)
    ACT_AS_PACKAGE_ONLY_CONANFILE = False

    def _is_package_only(self):
        return (
            self.ACT_AS_PACKAGE_ONLY_CONANFILE
            # The environment variable below can be used
            # to run conan create localy (used for debugging issues).
            or os.environ.get("@{names.cmake_var_suffix_upper}_CONAN_PACKAGING") == "ON"
        )

    def requirements(self):
        # TODO: add your libraries here
        self.requires("fmt/[~10]")

    def build_requirements(self):
        if not self._is_package_only():
            self.test_requires("gtest/1.14.0")

#%if not @header_only
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

#%end if
    def validate(self):
        minimal_cpp_standard = "17"
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, minimal_cpp_standard)
        minimal_version = self._compiler_support_lut()

        compiler = str(self.settings.compiler)
        if compiler not in minimal_version:
            self.output.warning(
                "%s recipe lacks information about the %s compiler standard version support" % (self.name, compiler))
            self.output.warning(
                "%s requires a compiler that supports at least C++%s" % (self.name, minimal_cpp_standard))
            return

        version = Version(self.settings.compiler.version)
        if version < minimal_version[compiler]:
            raise ConanInvalidConfiguration("%s requires a compiler that supports at least C++%s" % (self.name, minimal_cpp_standard))

    def layout(self):
        cmake_layout(self, src_folder=".", build_folder=".")
        self.folders.generators = ""

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["@{names.cmake_var_suffix_upper}_INSTALL"] = True
        tc.variables[
            "@{names.cmake_var_suffix_upper}_BUILD_TESTS"
        ] = not self._is_package_only()

        tc.generate()

        cmake_deps = CMakeDeps(self)
        cmake_deps.generate()

#%if @header_only
    def package_id(self):
        self.info.clear()

#%end if
    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder=self.source_folder)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "@{names.cmake_project_name}")
        self.cpp_info.set_property("cmake_target_name", "@{names.cmake_project_name}::@{names.styled_name}")

        self.cpp_info.names["cmake_find_package"] = "MyTestLib"
        self.cpp_info.names["cmake_find_package_multi"] = "MyTestLib"

#%if @corporate_tag
        component_name = "@{names.styled_name}"
#%else
        component_name = "_@{names.styled_name}"
#%end if

        self.cpp_info.components[component_name].set_property("cmake_target_name", "@{names.cmake_alias_target_name}")

        self.cpp_info.components[component_name].names["cmake_find_package"] = "@{names.conan_package_name}"
        self.cpp_info.components[component_name].names["cmake_find_package_multi"] = "@{names.conan_package_name}"
        self.cpp_info.components[component_name].set_property("cmake_target_name", "@{names.cmake_alias_target_name}")
        self.cpp_info.components[component_name].set_property("pkg_config_name", "@{names.cmake_alias_target_name}")


        # TODO: consider adding alloaces
        # self.cpp_info.components[component_name].set_property("cmake_target_aliases", [f"{self.name}::{self.name}"])
#%if not @header_only
        self.cpp_info.components[component_name].libs = ["@{names.cmake_project_name}"]
#%end if

        self.cpp_info.components[component_name].requires = [
            # TODO: add dependencies here.
            "fmt::fmt"
        ]

        # OS dependent settings
        # Here is an example:
        # if self.settings.os in ["Linux", "FreeBSD"]:
        #     self.cpp_info.components[component_name].system_libs.append("m")
        #     self.cpp_info.components[component_name].system_libs.append("pthread")
