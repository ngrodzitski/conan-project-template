#include <${names.src_path_prefix}/impl/helpers.hpp>

#include <gtest/gtest.h>

namespace /* anonymous */
{

// NOLINTNEXTLINE
using namespace ${names.cpp_namespace};

// NOLINTNEXTLINE
//#if "corporate_tag_camel" in self.keys()
TEST( ${corporate_tag_camel}${camel_name}ImplHelpers, MakeCanonicalName )
//#else
TEST( ${camel_name}ImplHelpers, MakeCanonicalName )
//#end if
{
    EXPECT_EQ( impl::${names.cpp_make_canonical_name_func}( "qwerty12345" ), "qwerty12345" );
    EXPECT_EQ( impl::${names.cpp_make_canonical_name_func}( "qwerty\r\n12345" ), "qwerty\\x0D\\x0A12345" );
}

}  // anonymous namespace
