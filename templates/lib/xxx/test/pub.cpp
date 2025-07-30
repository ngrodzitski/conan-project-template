#include <${names.src_path_prefix}/pub.hpp>

#include <gtest/gtest.h>

namespace /* anonymous */
{

// NOLINTNEXTLINE
using namespace ${names.cpp_namespace};

// NOLINTNEXTLINE
//#if "corporate_tag_camel" in self.keys()
TEST( ${corporate_tag_camel}${camel_name}, MakeCanonicalSample )
//#else
TEST( ${camel_name}, MakeCanonicalSample )
//#end if
{
    EXPECT_EQ( ${names.cpp_make_canonical_sample_func}( "xyz" ).name(), "xyz" );
    EXPECT_EQ( ${names.cpp_make_canonical_sample_func}( "x\xFFyz" ).name(), "x\\xFFyz" );
}

//#if "corporate_tag_camel" in self.keys()
TEST( ${corporate_tag_camel}${camel_name}, Format )
//#else
TEST( ${camel_name}, Format )
//#end if
{
    EXPECT_EQ( fmt::format("{}", ${names.cpp_make_canonical_sample_func}( "xyz" ) ), "{ xyz }" );
    EXPECT_EQ( fmt::format("{}", ${names.cpp_make_canonical_sample_func}( "x\xFFyz" ) ), "{ x\\xFFyz }" );
}

}  // anonymous namespace
