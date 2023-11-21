#include <${src_path_prefix}${name}/version.hpp>

#include <iostream>
#include <filesystem>

#include <fmt/format.h>

namespace ${cpp_namespace_prefix}${name} {

namespace fs = std::filesystem;

//
// main()
//

int main(int argc, const char** argv)
{
    // TODO: Insert your logic here.

//#if "corporate_tag" in self.keys()
//#set $macro_prefix = $corporate_tag.upper() + "_" + $name.upper()
//#set $ctag = $corporate_tag.lower()
//#else
//#set $macro_prefix = $name.upper()
//#set $ctag = ""
//#end if
    std::cout << fmt::format( "{} v{}.{}.{}",
                              fs::path( argv[ 0 ] ).filename().native(),
                              ${macro_prefix}_VERSION_MAJOR,
                              ${macro_prefix}_VERSION_MINOR,
                              ${macro_prefix}_VERSION_PATCH ) << std::endl;

    for( int i=1; i < argc; ++i )
    {
        std::cout << fmt::format("argv[{}]: {}", i, argv[i] ) << std::endl;

    }

    return 0;
}

}  // namespace ${cpp_namespace_prefix}${name}
