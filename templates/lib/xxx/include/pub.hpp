#pragma once

#include <string>
#include <string_view>
//#if $header_only
#include <numeric>
//#end if

#include <fmt/format.h>

namespace ${names.cpp_namespace}
{

//
// ${names.cpp_sample_class_name}
//

/**
 * @brief Sample class for ${names.styled_name} library.
 *
 * That is documunation for it.
 */
class ${names.cpp_sample_class_name}
{
public:
//#if $header_only
    ${names.cpp_sample_class_name}(std::string name)
        : m_name{ std::move( name ) }
    {}
//#else
    ${names.cpp_sample_class_name}(std::string name);
//#end if

    /**
     * @brief Name of the instance.
     */
    const std::string& name() const noexcept { return m_name; }

private:
    /**
     * @brief Name of the instance.
     *
     * That is just for demo purposes.
     */
    std::string m_name;
};

//#if $header_only
namespace details
{

//
// ${names.cpp_make_canonical_name_func}()
//

inline std::string ${names.cpp_make_canonical_name_func}( std::string_view name )
{
    constexpr char ${names.cpp_hex_digits_var}[] = "0123456789ABCDEF";
    std::string result;
    result.reserve( name.size() + std::accumulate(begin(name),
                    end(name),
                    0,
                    [](auto memo, auto ch) {
                        return memo + (std::isprint(ch) ? 1 : 4);
                    }));

    for( const auto ch : name )
    {
        if( std::isprint( ch ) )
        {
            result += ch;
        }
        else
        {
            const auto code = static_cast<std::uint8_t>(ch);
            result += '\\';
            result += 'x';
            result += ${names.cpp_hex_digits_var}[code >> 4];
            result += ${names.cpp_hex_digits_var}[code & 0x0F];
        }
    }

    return result;
}

}  // namespace details
//#end if

//
// ${names.cpp_make_canonical_sample_func}()
//

/**
 * @brief Make canonical instance for a given name
 *
 * @return An instance of ${names.cpp_sample_class_name} with caonical name.
 */
//#if $header_only
inline ${names.cpp_sample_class_name} ${names.cpp_make_canonical_sample_func}( std::string_view name )
{
    return ${names.cpp_sample_class_name}{ details::${names.cpp_make_canonical_name_func}( name ) };
}
//#else
${names.cpp_sample_class_name} ${names.cpp_make_canonical_sample_func}(std::string_view name);
//#end if

}  // namespace ${names.cpp_namespace}

namespace fmt
{

template <>
struct formatter<${names.cpp_namespace}::${names.cpp_sample_class_name}> {
    template <class Parse_Context>
    constexpr auto parse(Parse_Context& ctx) {
        auto it = std::begin(ctx);
        auto end = std::end(ctx);
        if (it != end && *it != '}') {
            throw fmt::format_error("invalid format");
        }
        return it;
    }

    template <class Format_Context>
    auto format(const ${names.cpp_namespace}::${names.cpp_sample_class_name}& s, Format_Context& ctx) {
        return format_to(ctx.out(), "{{ {} }}", s.name());
    }
};

}  // namespace fmt
