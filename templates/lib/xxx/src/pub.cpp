#include <${names.src_path_prefix}/pub.hpp>

#include <${names.src_path_prefix}/impl/helpers.hpp>

namespace ${names.cpp_namespace}
{

//
// ${names.cpp_sample_class_name}
//

${names.cpp_sample_class_name}::${names.cpp_sample_class_name}( std::string name )
    : m_name{ std::move(name) }
{}

//
// ${names.cpp_make_canonical_sample_func}()
//

/**
 * @brief Make canonical instance for a given name
 *
 * @return An instance of ${names.cpp_sample_class_name} with caonical name.
 */
${names.cpp_sample_class_name} ${names.cpp_make_canonical_sample_func}( std::string_view name )
{
    return ${names.cpp_sample_class_name}{ impl::${names.cpp_make_canonical_name_func}( name ) };
}

}  // namespace ${names.cpp_namespace}
