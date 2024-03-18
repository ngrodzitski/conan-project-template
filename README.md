# conan-project-template

A generator for conan-based projects.

Allows to generate an initial structure of the project (library)
that uses Conan that includes all boring stuff (cmake-scripts, initial sample sources)
and is ready for further development

```txt
usage: project_generator.py [-h] -t project-type -d dir-path -n name -N camel-name [--header-only] [--corporate-tag corporate-tag]

Generate conan-based project stub (a starter)

optional arguments:
  -h, --help            show this help message and exit
  -t project-type, --project-type project-type
                        Project type (allowed values: 'app', 'lib')
  -d dir-path, --dir-path dir-path
                        Directory where to generate a stub project
  -n name, --name name  Project name
  -N camel-name, --camel-name camel-name
                        CamelNaming project name (used in 'conanfile.py')
  --header-only         The library is header-only
  --corporate-tag corporate-tag
                        Add a corporate tag, used as a top level namespace
```

## Create library

Example commands to create a library.

```bash
# Create library project:
python ./project_generator.py -t lib -n cool_lib -N CoolLib -d /tmp/cool_lib

# Or:
python ./project_generator.py \
     --project-type lib \
     --name cool_lib \
     --camel-name CoolLib \
     --dir-path /tmp/cool_lib

# Header only:
python ./project_generator.py \
     --project-type lib \
     --name cool_lib \
     --camel-name CoolLib \
     --dir-path /tmp/cool_lib \
     --header-only

# With corporate tag:
python ./project_generator.py \
     --project-type lib \
     --name cool_lib \
     --camel-name CoolLib \
     --dir-path /tmp/cool_lib \
     --corporate-tag kola
```

# Build instructions

Sample commands to build the generated project

On Linux:

```bash
conan install . -pr:a my_profile --build missing -of build_dir
(source ./build_dir/conanbuild.sh && cmake -Bbuild_dir . -DCMAKE_TOOLCHAIN_FILE=build_dir/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release)
cmake --build build_dir -j $(nproc) --verbose

# Build with ubu-gcc11 profile
conan install . -pr:a ubu-gcc11 --build missing -s:a build_type=Debug -of _build
(source ./_build/conanbuild.sh && cmake -B_build . -DCMAKE_TOOLCHAIN_FILE=_build/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Debug)
cmake --build _build -j 6 --verbose
```
On Windows:

```cmd
conan install . -pr:a my_profile --build missing -of build_dir
build_dir/conanbuild.bat
cmake -Bbuild_dir . -DCMAKE_TOOLCHAIN_FILE=build_dir/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release
cmake --build build_dir -j %NUMBER_OF_PROCESSORS% --verbose --config Release

# Build with vs2022 profile
conan install . -pr:a vs2022 --build missing -s:a build_type=Debug -of _build
./_build/conanbuild.bat
cmake -B_build . -DCMAKE_TOOLCHAIN_FILE=_build/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Debug
cmake --build _build -j 6 --verbose --config Debug
```
