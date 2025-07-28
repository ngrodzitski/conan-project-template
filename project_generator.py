import argparse
import re
import os
import json
import shutil
from pathlib import Path
from Cheetah.Template import Template

try:
    from prettytable import PrettyTable

    pretty_table_available = True
except ImportError:
    pretty_table_available = False


def print_params(args):

    print("Generate project stub...")
    if pretty_table_available:
        table = PrettyTable()
        table.field_names = ["Parameter", "Value"]

        table.add_row(["Project type", args.project_type])
        table.add_row(["Target directory", args.dir_path])
        table.add_row(["snake_case project name", args.name])
        table.add_row(["CamelCase project name", args.camel_name])

        table.add_row(["Style", args.style])

        if args.project_type == "app":
            table.add_row(["Qt QML", args.qml])

        if args.project_type == "lib":
            table.add_row(["Header-only", args.header_only])

        table.add_row(["Corporate tag", args.corporate_tag])

        print(table)
    else:
        print("=" * 60)
        print(f"Project type: {args.project_type}")
        print(f"Generating stub project in directory: {args.dir_path}")
        print(f"snake_case project name: {args.name}")
        print(f"Camel Naming project name: {args.camel_name}")
        print(f"Style: {args.style}")
        if args.project_type == "app":
            print(f"Qt QML: {args.header_only}")
        if args.project_type == "lib":
            print(f"Header Only: {args.header_only}")

        print(f"Corporate tag: {args.corporate_tag}")
        print("=" * 60)


# Generate Markdown/Python/Cmake content from template
def generate_md_py_cmake_piece(template_file, params):
    template = Template.compile(
        file=template_file,
        compilerSettings=dict(
            cheetahVarStartToken="@",
            directiveStartToken="#%",
            directiveEndToken="#%",
            commentStartToken="##",
        ),
        baseclass=dict,
        useCache=False,
    )
    return str(template(params))

# Generate Markdown/Python/Cmake content from template
def generate_cpp_piece(template_file, params):
    template = Template.compile(
        file=template_file,
        compilerSettings=dict(
            directiveStartToken="//#",
            directiveEndToken="//#",
            commentStartToken="//##",
        ),
        baseclass=dict,
        useCache=False,
    )
    return str(template(params))


def print_gen_file_report(src, dest):
    print(f"[GEN] $(gen-root)/{src}{' '*max([40 -len(src), 1])} => {dest}")

def copy_static_files(dest_dir, src_dir, fnames):
    print(f"[CALL] copy_static_files({dest_dir}, {src_dir}, ...)\n\n")
    for fname in fnames:
        dest_file_path=os.path.join(dest_dir, fname)
        Path(dest_file_path).parent.mkdir(parents=True, exist_ok=True)
        src_file_path=os.path.join(src_dir, fname)
        shutil.copy2(src_file_path, dest_file_path)
        print_gen_file_report(f"static/{fname}", dest_file_path)

class GeneratorRunner:
    def __init__(self, dest_dir, template_src_dir, gen_params):
        self.dest_dir = dest_dir
        self.template_src_dir = template_src_dir
        self.gen_params = gen_params

    def generate_file(self, src_template, dest_path, generate_piece):
        dest_file_path=os.path.join(self.dest_dir, dest_path)
        template_file_path=os.path.join(self.template_src_dir, src_template)

        dest_dir = os.path.dirname(os.path.abspath(dest_file_path))
        os.makedirs(dest_dir, exist_ok=True)
        print_gen_file_report(f"templates/{src_template}", dest_file_path)

        content = generate_piece(template_file_path, self.gen_params)
        with open(dest_file_path, "w") as file:
            # Write the content to the file:
            file.write(content)

def generate_stub_project(args):
    print_params(args)

    template_src_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "templates",
        args.project_type,
    )
    print(f"Base templates dir: {template_src_dir}")

    static_src_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "static"
    )
    print(f"Base static files dir: {static_src_dir}")

    dest_dir = args.dir_path
    if not os.path.exists(dest_dir):
        Path(dest_dir).mkdir(parents=True)

    gen_params = {
        "name": args.name,
        "camel_name": args.camel_name,
        "styled_name": args.camel_name if args.style == "Camel" else args.name ,
        "style": args.style,
        "qml": args.qml,
        "header_only": args.header_only,
    }

    if args.corporate_tag:
        corporate_tag_normalized_word = args.corporate_tag.replace("::", "_")
        corporate_tag_normalized_path = args.corporate_tag.replace("::", "/")
        gen_params["PROJECT_CMAKE_VAR_SUFFIX"] = corporate_tag_normalized_word.upper()
        gen_params["project_cmake_var_suffix"] = corporate_tag_normalized_word.lower()
        gen_params["corporate_tag_cammel"] = args.corporate_tag.replace("::"," ").title().replace(" ", "")
        gen_params["corporate_tag_normalized_word"] = corporate_tag_normalized_word
        gen_params["corporate_tag_normalized_path"] = corporate_tag_normalized_path
        if args.project_type == "lib":
            gen_params["library_macros"] = f"{corporate_tag_normalized_word.upper()}_LIB_{args.name.upper()}"

        gen_params["src_path_prefix"] = f"{corporate_tag_normalized_path}/"
        gen_params["cpp_namespace_prefix"] = f"{args.corporate_tag}::"
    else:
        gen_params["PROJECT_CMAKE_VAR_SUFFIX"] = args.name.upper()
        gen_params["project_cmake_var_suffix"] = args.name.lower()
        if args.project_type == "lib":
            gen_params["library_macros"] = f"LIB_{args.name.upper()}"
        gen_params["src_path_prefix"] = ""
        gen_params["cpp_namespace_prefix"] = ""

    copy_static_files(
        dest_dir = dest_dir,
        src_dir = static_src_dir,
        fnames = [".gitignore", ".clang-format"]
    )

    gen = GeneratorRunner( dest_dir, template_src_dir, gen_params)

    if (args.qml):
        copy_static_files(
            dest_dir = os.path.join(dest_dir, gen_params['styled_name']),
            src_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "templates/app/xxx"),
            fnames = ["qml/MyButton.qml",
                      "images/sample_image.png",
                      "js/CommonUtils.js",
                      "fonts/blocks-3x3-monospaced.ttf"] )
        gen.generate_file(
            "xxx/qml/MyMainWindow.qml",
            f"{gen_params['styled_name']}/qml/MyMainWindow.qml",
            generate_md_py_cmake_piece
        )

    gen.generate_file( "README.md", "README.md", generate_md_py_cmake_piece)
    gen.generate_file( "CMakeLists.txt", "CMakeLists.txt", generate_md_py_cmake_piece)
    gen.generate_file( "conanfile.py", "conanfile.py", generate_md_py_cmake_piece)
    gen.generate_file( "xxx/CMakeLists.txt", f"{gen_params['styled_name']}/CMakeLists.txt", generate_md_py_cmake_piece)

    gen.generate_file(
        "xxx/include/version.hpp",
        f"{gen_params['styled_name']}/include/{gen_params['src_path_prefix']}{gen_params['styled_name']}/version.hpp",
        generate_cpp_piece
    )

    if args.project_type == "lib":
        gen.generate_file(
            "xxx/include/pub.hpp",
            f"{gen_params['styled_name']}/include/{gen_params['src_path_prefix']}{gen_params['styled_name']}/pub.hpp",
            generate_cpp_piece
        )

        if not args.header_only:
            gen.generate_file(
                "xxx/src/pub.cpp",
                f"{gen_params['styled_name']}/src/{gen_params['src_path_prefix']}{gen_params['styled_name']}/pub.cpp",
                generate_cpp_piece
            )
            gen.generate_file(
                "xxx/include/impl/helpers.hpp",
                f"{gen_params['styled_name']}/include/{gen_params['src_path_prefix']}{gen_params['styled_name']}/impl/helpers.hpp",
                generate_cpp_piece
            )
            gen.generate_file(
                "xxx/src/impl/helpers.cpp",
                f"{gen_params['styled_name']}/src/{gen_params['src_path_prefix']}{gen_params['styled_name']}/impl/helpers.cpp",
                generate_cpp_piece
            )

        gen.generate_file(
            "xxx/test/CMakeLists.txt",
            f"{gen_params['styled_name']}/test/CMakeLists.txt",
            generate_md_py_cmake_piece
        )
        gen.generate_file(
            "xxx/test/pub.cpp",
            f"{gen_params['styled_name']}/test/pub.cpp",
            generate_cpp_piece
        )
        if not args.header_only:
            gen.generate_file(
                "xxx/test/impl/helpers.cpp",
                f"{gen_params['styled_name']}/test/impl/helpers.cpp",
                generate_cpp_piece
            )
        gen.generate_file(
            "xxx/cmake/lib-config.cmake.in",
            f"{gen_params['styled_name']}/cmake/lib-config.cmake.in",
            generate_md_py_cmake_piece
        )

        gen.generate_file(
            "test_package/CMakeLists.txt",
            "test_package/CMakeLists.txt",
            generate_md_py_cmake_piece
        )
        gen.generate_file(
            "test_package/conanfile.py",
            "test_package/conanfile.py",
            generate_md_py_cmake_piece
        )
        gen.generate_file(
            "test_package/example.cpp",
            "test_package/example.cpp",
            generate_cpp_piece
        )

    if args.project_type == "app":
        gen.generate_file(
            "xxx/include/main.hpp",
            f"{gen_params['styled_name']}/include/{gen_params['src_path_prefix']}{gen_params['styled_name']}/main.hpp",
            generate_cpp_piece
        )
        gen.generate_file(
            "xxx/src/main_lib.cpp",
            f"{gen_params['styled_name']}/src/{gen_params['src_path_prefix']}{gen_params['styled_name']}/main.cpp",
            generate_cpp_piece
        )
        gen.generate_file(
            "xxx/src/main_exe.cpp",
            f"{gen_params['styled_name']}/src/main.cpp",
            generate_cpp_piece
        )

        gen.generate_file(
            "xxx/test/CMakeLists.txt",
            f"{gen_params['styled_name']}/test/CMakeLists.txt",
            generate_md_py_cmake_piece
        )

        sample_test_name = "SampleTest" if args.style == "Camel" else "sample_test"
        gen.generate_file(
            "xxx/test/sample_test.cpp",
            f"{gen_params['styled_name']}/test/{sample_test_name}.cpp",
            generate_cpp_piece
        )

    print( """To build the project you can use the following commands:

# Linux

conan install . -pr:a my_profile --build missing -of build_dir
(source ./build_dir/conanbuild.sh && cmake -Bbuild_dir . -DCMAKE_TOOLCHAIN_FILE=build_dir/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release)
cmake --build build_dir -j $(nproc) --verbose

# Build with ubu-gcc-11 profile
conan install . -pr:a ubu-gcc-11 --build missing -s:a build_type=Debug -of _build
(source ./_build/conanbuild.sh && cmake -B_build . -DCMAKE_TOOLCHAIN_FILE=_build/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Debug)
cmake --build _build -j 6 --verbose

# Windows

conan install . -pr:a my_profile --build missing -of build_dir
build_dir/conanbuild.bat
cmake -Bbuild_dir . -DCMAKE_TOOLCHAIN_FILE=build_dir/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release
cmake --build build_dir -j %NUMBER_OF_PROCESSORS% --verbose

# Build with vs2022 profile
conan install . -pr:a vs2022 --build missing -s:a build_type=Debug -of _build
_build\conanbuild.bat
cmake -B_build . -DCMAKE_TOOLCHAIN_FILE="_build\conan_toolchain.cmake" -DCMAKE_BUILD_TYPE=Debug
cmake --build _build -j 6 --verbose --config Debug
""")


class CheckNiceCIdentifierAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        # Require to start with letter, even though "_"
        # is a legit first character for c-idntifier, but it is an odd name
        # we would like to avoid.
        pattern = re.compile(r"^[a-zA-Z]\w*$")

        if not bool(pattern.match(value)):
            raise argparse.ArgumentError(
                self, f"not nice c identifier: '{value}'"
            )
        setattr(namespace, self.dest, value)

class CheckNiceCIdentifierWithNsAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        # Require to start with letter, even though "_"
        # is a legit first character for c-idntifier, but it is an odd name
        # we would like to avoid.
        pattern = re.compile(r"^[a-zA-Z]\w*$")

        for substr in value.split("::"):
            if substr == "" or not bool(pattern.match(substr)):
                raise argparse.ArgumentError(
                    self, f"not nice c identifier with namespace: '{value}'"
                )

        setattr(namespace, self.dest, value)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate conan-based project stub (a starter)"
    )
    parser.add_argument(
        "-t",
        "--project-type",
        choices=["app", "lib"],
        metavar="project-type",
        help="Project type (allowed values: 'app', 'lib')",
        required=True,
    )
    parser.add_argument(
        "--qml",
        action="store_true",
        help="Create a Qt QML application",
        default=False,
    )
    parser.add_argument(
        "--style",
        choices=["Camel", "snake"],
        metavar="style",
        help="Use snake_case (default) or CamelCase, (allowed values: 'snake', 'Camel') ",
        default='snake_case',
    )
    parser.add_argument(
        "-d",
        "--dir-path",
        metavar="dir-path",
        help="Directory where to generate a stub project",
        required=True,
    )
    parser.add_argument(
        "-n",
        "--name",
        metavar="name",
        help="Project name",
        required=True,
        action=CheckNiceCIdentifierAction,
    )
    parser.add_argument(
        "-N",
        "--camel-name",
        metavar="camel-name",
        help="CamelNaming project name (used in 'conanfile.py')",
        required=True,
        action=CheckNiceCIdentifierAction,
    )

    parser.add_argument(
        "--header-only",
        action="store_true",
        help="The library is header-only",
        default=False,
    )
    parser.add_argument(
        "--corporate-tag",
        metavar="corporate-tag",
        help="Add a corporate tag, used as a top level namespace",
        action=CheckNiceCIdentifierWithNsAction
    )

    args = parser.parse_args()

    if args.project_type == 'app':
        if args.header_only:
            raise argparse.ArgumentError(
                self, f"header-only option is only applicable to lib projects"
            )

    if args.project_type == 'lib':
        if args.qml:
            raise argparse.ArgumentError(
                self, f"qml option is only applicable to app projects"
            )

    generate_stub_project(args)
