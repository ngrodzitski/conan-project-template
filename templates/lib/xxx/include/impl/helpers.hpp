#pragma once

#include <string>
#include <string_view>

namespace ${cpp_namespace_prefix}${name}::impl {

//
// make_canonical_name()
//

/**
 * @brief Make canonical name
 *
 * For demo let's consider conanical as one with no unprinted characters.
 */
std::string make_canonical_name( std::string_view name );

}  // namespace ${cpp_namespace_prefix}${name}::impl
