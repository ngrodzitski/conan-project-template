#include <${src_path_prefix}${name}/main.hpp>

#include <gtest/gtest.h>

namespace /* anonymous */
{

// NOLINTNEXTLINE
//#if "corporate_tag_cammel" in self.keys()
TEST( ${corporate_tag_cammel}${camel_name}, SampleTest )
//#else
TEST( ${camel_name}, SampleTest )
//#end if
{
    EXPECT_TRUE(true);
}

}  // anonymous namespace
