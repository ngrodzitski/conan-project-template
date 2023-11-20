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

#%if not @header_only
    options = {
        "fPIC": [True, False],
    }
    default_options = {
        "fPIC": True,
    }

#%end if
#%if "corporate_tag" in self.keys()
    name = "@{corporate_tag.lower()}@{name}"
#%else
    name = "@{name}"
#%end if

    license = "TODO"
    author = "TODO"
    url = "TODO"
    homepage = "TODO"
    description = "@{name} library"

    topics = ("@{name}", "todo")

    generators = "cmake_find_package", "cmake"
    settings = "os", "compiler", "build_type", "arch"

    exports_sources = [
        "CMakeLists.txt",
        "@{name}/*",
        "cmake-scripts/*"
    ]
    no_copy_source = False
    build_policy = "missing"
    _cmake = None

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
#%if "corporate_tag" in self.keys()
            or os.environ.get("@{corporate_tag.upper()}_CONAN_PACKAGING") == "ON"
#%else
            or os.environ.get("@{name.upper()}_CONAN_PACKAGING") == "ON"
#%end if
        )

    def requirements(self):
        # TODO: add your libraries here
        self.requires("fmt/[~10]")

    def build_requirements(self):
        if not self._is_package_only():
            self.build_requires("gtest/1.14.0")

#%if not @header_only
    def package_id(self):
        self.info.clear()

#%end if
    def configure(self):
        minimal_cpp_standard = "17"
        if self.settings.compiler.cppstd:
            tools.check_min_cppstd(self, minimal_cpp_standard)
        minimal_version = {
            "gcc": "9",
            "clang": "10",
        }
        compiler = str(self.settings.compiler)
        if compiler not in minimal_version:
            self.output.warn(
                (
                    "%s recipe lacks information about the %s compiler "
                    "standard version support"
                )
                % (self.name, compiler)
            )
            self.output.warn(
                "%s requires a compiler that supports at least C++%s"
                % (self.name, minimal_cpp_standard)
            )
            return

        version = tools.Version(self.settings.compiler.version)
        if version < minimal_version[compiler]:
            raise ConanInvalidConfiguration(
                "%s requires a compiler that supports at least C++%s"
                % (self.name, minimal_cpp_standard)
            )

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake

        self._cmake = CMake(self)
        self._cmake.definitions["@{PROJECT_CMAKE_VAR_SUFFIX}_INSTALL"] = True
        self._cmake.definitions["@{PROJECT_CMAKE_VAR_SUFFIX}_CONAN_BUILD"] = True
        self._cmake.definitions[
            "@{PROJECT_CMAKE_VAR_SUFFIX}_BUILD_TESTS"
        ] = not self._is_package_only()

        self._cmake.configure()
        return self._cmake

    def build(self):
#%if @header_only
        pass
#%else
        cmake = self._configure_cmake()
        cmake.build()
#%end if

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.components["@{name}"].names["cmake_find_package"] = self.name
        self.cpp_info.components["@{name}"].names["cmake_find_package_multi"] = self.name
#%if not @header_only
        self.cpp_info.components["@{name}"].libs = [self.name]
#%end if
        self.cpp_info.components["@{name}"].requires = [
            # TODO: add your libraries here.
            "fmt::fmt",
        ]
        self.cpp_info.components[
            "@{name}"
        ].set_property("cmake_target_name", f"{self.name}::@{name}")
        self.cpp_info.components["@{name}"].defines.append(
            "@{library_macros}"
        )
