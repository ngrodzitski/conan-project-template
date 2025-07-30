#pragma once

#include <string>
#include <string_view>

namespace ${names.cpp_namespace}::impl
{

//
// ${names.cpp_make_canonical_name_func}()
//

/**
 * @brief Make canonical name.
 *
 * For demo let's consider conanical as one with no unprinted characters.
 */
std::string ${names.cpp_make_canonical_name_func}( std::string_view name );

}  // namespace ${names.cpp_namespace}::impl
