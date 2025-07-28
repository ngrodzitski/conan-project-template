// An entry point for executable.
// The core application logic is in the library
// to which this executable is linked to.

#include <iostream>

#include <${src_path_prefix}${styled_name}/main.hpp>

int main(int argc, char** argv) {
    try {
        // TODO:
        // Consider to rune globaly effective init routines
        return ${cpp_namespace_prefix}${styled_name}::main(argc, argv);
    } catch ( const std::exception & ex ) {
        std::cerr << "Error: " << ex.what() << std::endl;
    } catch (...) {
        // TODO:
        // Handle exceptions here.
        return -1;
    }
}
