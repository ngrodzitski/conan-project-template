#include <iostream>

#include <${src_path_prefix}${name}/version.hpp>
#include <${src_path_prefix}${name}/pub.hpp>

int main() {
//#if hasattr(self,"corporate_tag")
//#set $macro_prefix = $corporate_tag.upper() + "_" + $name.upper()
//#set $ctag = $corporate_tag.lower()
//#else
//#set $macro_prefix = $name.upper()
//#set $ctag = ""
//#end if
    std::cout << "Welcome to ${name} ("
              << "v" << ${macro_prefix}_VERSION_MAJOR << "." << ${macro_prefix}_VERSION_MINOR << "."
              << ${macro_prefix}_VERSION_PATCH << " rev: " << ${macro_prefix}_VCS_REVISION "), "
              << "package is provided by Conan V1!\n";
}
