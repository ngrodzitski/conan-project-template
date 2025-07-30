#include <iostream>

#include <${names.src_path_prefix}/version.hpp>
#include <${names.src_path_prefix}/pub.hpp>

int main() {
//#if "corporate_tag_normalized_word" in self.keys()
//#set $macro_prefix = $corporate_tag_normalized_word.upper() + "_" + $name.upper()
//#else
//#set $macro_prefix = $name.upper()
//#end if
    std::cout << "Welcome to ${styled_name} ("
              << "v" << ${macro_prefix}_VERSION_MAJOR << "." << ${macro_prefix}_VERSION_MINOR << "."
              << ${macro_prefix}_VERSION_PATCH << " rev: " << ${macro_prefix}_VCS_REVISION "), "
              << "package is provided by Conan V2!\n";
}
