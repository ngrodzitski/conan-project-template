import argparse
import re
import os
import json
import shutil
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
        table.add_row(["Project name", args.name])
        table.add_row(["CamelCase project name", args.camel_name])

        if args.project_type == "lib":
            table.add_row(["Header-only", args.header_only])

        table.add_row(["Corporate tag", args.corporate_tag])

        print(table)
    else:
        print("=" * 60)
        print(f"Project type: {args.project_type}")
        print(f"Generating stub project in directory: {args.dir_path}")
        print(f"Project name: {args.name}")
        print(f"Camel Naming project name: {args.camel_name}")
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
    for fname in fnames:
        dest_file_path=os.path.join(dest_dir, fname)
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
        os.mkdir(dest_dir)

    gen_params = {
        "name": args.name,
        "camel_name": args.camel_name,
        "header_only": args.header_only,
    }

    if args.corporate_tag:
        gen_params["PROJECT_CMAKE_VAR_SUFFIX"] = args.corporate_tag.upper()
        gen_params["project_cmake_var_suffix"] = args.corporate_tag.lower()
        gen_params["corporate_tag"] = args.corporate_tag
        if args.project_type == "lib":
            gen_params["library_macros"] = f"{args.corporate_tag.upper()}_LIB_{args.name.upper()}"

        gen_params["src_path_prefix"] = f"{args.corporate_tag}/"
        gen_params["cpp_namespace_prefix"] = f"{args.corporate_tag}::"
    else:
        gen_params["PROJECT_CMAKE_VAR_SUFFIX"] = args.name.upper()
        gen_params["project_cmake_var_suffix"] = args.name.lower()
        if args.project_type == "lib":
            gen_params["library_macros"] = f"LIB_{args.name.upper()}"
        gen_params["src_path_prefix"] = ""
        gen_params["cpp_namespace_prefix"] = ""

    gen = GeneratorRunner( dest_dir, template_src_dir, gen_params)


    gen.generate_file( "README.md", "README.md", generate_md_py_cmake_piece)
    gen.generate_file( "CMakeLists.txt", "CMakeLists.txt", generate_md_py_cmake_piece)
    gen.generate_file( "conanfile.py", "conanfile.py", generate_md_py_cmake_piece)

    gen.generate_file( "xxx/CMakeLists.txt", f"{gen_params['name']}/CMakeLists.txt", generate_md_py_cmake_piece)
    gen.generate_file(
        "xxx/include/pub.hpp",
        f"{gen_params['name']}/include/{gen_params['src_path_prefix']}{gen_params['name']}/pub.hpp",
        generate_cpp_piece
    )
    gen.generate_file(
        "xxx/include/version.hpp",
        f"{gen_params['name']}/include/{gen_params['src_path_prefix']}{gen_params['name']}/version.hpp",
        generate_cpp_piece
    )

    if not args.header_only:
        gen.generate_file(
            "xxx/src/pub.cpp",
            f"{gen_params['name']}/src/{gen_params['src_path_prefix']}{gen_params['name']}/pub.cpp",
            generate_cpp_piece
        )
        gen.generate_file(
            "xxx/include/impl/helpers.hpp",
            f"{gen_params['name']}/include/{gen_params['src_path_prefix']}{gen_params['name']}/impl/helpers.hpp",
            generate_cpp_piece
        )
        gen.generate_file(
            "xxx/src/impl/helpers.cpp",
            f"{gen_params['name']}/src/{gen_params['src_path_prefix']}{gen_params['name']}/impl/helpers.cpp",
            generate_cpp_piece
        )

    gen.generate_file(
        "xxx/test/CMakeLists.txt",
        f"{gen_params['name']}/test/CMakeLists.txt",
        generate_md_py_cmake_piece
    )
    gen.generate_file(
        "xxx/test/pub.cpp",
        f"{gen_params['name']}/test/pub.cpp",
        generate_cpp_piece
    )
    if not args.header_only:
        gen.generate_file(
            "xxx/test/impl/helpers.cpp",
            f"{gen_params['name']}/test/impl/helpers.cpp",
            generate_cpp_piece
        )
    gen.generate_file(
        "xxx/cmake/lib-config.cmake.in",
        f"{gen_params['name']}/cmake/lib-config.cmake.in",
        generate_md_py_cmake_piece
    )

    copy_static_files(
        dest_dir = dest_dir,
        src_dir = static_src_dir,
        fnames = [".gitignore", ".clang-format"]
    )

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
        action=CheckNiceCIdentifierAction
    )

    generate_stub_project(parser.parse_args())
