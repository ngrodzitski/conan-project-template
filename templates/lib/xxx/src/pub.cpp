#include <${src_path_prefix}${name}/pub.hpp>

#include <${src_path_prefix}${name}/impl/helpers.hpp>

namespace ${cpp_namespace_prefix}${name}
{

//
// sample_class_t
//

sample_class_t::sample_class_t( std::string name ) : m_name{ std::move(name) } {}

//
// make_canonical_sample()
//

/**
 * @brief Make canonical instance for a given name
 *
 * @return An instance of sample_class_t with caonical name.
 */
sample_class_t make_canonical_sample( std::string_view name )
{
    return sample_class_t{ impl::make_canonical_name( name ) };
}

}  // namespace ${cpp_namespace_prefix}${name}
