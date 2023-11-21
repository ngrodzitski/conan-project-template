// An entry point for executable.
// The core application logic is in the library
// to which this executable is linked to.

#include <iostream>

#include <${src_path_prefix}${name}/main.hpp>

int main(int argc, const char** argv) {
    try {
        // TODO:
        // Consider to rune globaly effective init routines
        return ${cpp_namespace_prefix}${name}::main(argc, argv);
    } catch (...) {
        // TODO:
        // Handle exceptions here.
        return -1;
    }
}
