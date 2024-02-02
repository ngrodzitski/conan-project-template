#include <${src_path_prefix}${name}/impl/helpers.hpp>

#include <gtest/gtest.h>

namespace /* anonymous */
{

// NOLINTNEXTLINE
using namespace ${cpp_namespace_prefix}${name};

// NOLINTNEXTLINE
//#if "corporate_tag_camel" in self.keys()
TEST( ${corporate_tag_camel}${camel_name}ImplHelpers, MakeCanonicalName )
//#else
TEST( ${camel_name}ImplHelpers, MakeCanonicalName )
//#end if
{
    EXPECT_EQ( impl::make_canonical_name( "qwerty12345" ), "qwerty12345" );
    EXPECT_EQ( impl::make_canonical_name( "qwerty\r\n12345" ), "qwerty\\x0D\\x0A12345" );
}

}  // anonymous namespace
