#include <${src_path_prefix}${name}/pub.hpp>

#include <gtest/gtest.h>

namespace /* anonymous */
{

// NOLINTNEXTLINE
using namespace ${cpp_namespace_prefix}${name};

// NOLINTNEXTLINE
//#if "corporate_tag_camel" in self.keys()
TEST( ${corporate_tag_camel}${camel_name}, MakeCanonicalSample )
//#else
TEST( ${camel_name}, MakeCanonicalSample )
//#end if
{
    EXPECT_EQ( make_canonical_sample( "xyz" ).name(), "xyz" );
    EXPECT_EQ( make_canonical_sample( "x\xFFyz" ).name(), "x\\xFFyz" );
}

//#if "corporate_tag_camel" in self.keys()
TEST( ${corporate_tag_camel}${camel_name}, Format )
//#else
TEST( ${camel_name}, Format )
//#end if
{
    EXPECT_EQ( fmt::format("{}", make_canonical_sample( "xyz" ) ), "{ xyz }" );
    EXPECT_EQ( fmt::format("{}", make_canonical_sample( "x\xFFyz" ) ), "{ x\\xFFyz }" );
}

}  // anonymous namespace
