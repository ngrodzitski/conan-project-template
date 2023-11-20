#pragma once

#include <string>
#include <string_view>
//#if $header_only
#include <numeric>
//#end if

#include <fmt/format.h>

namespace ${cpp_namespace_prefix}${name}
{

//
// sample_class_t
//

/**
 * @brief Sample class for ${name} library.
 *
 * That is documunation for it.
 */
class sample_class_t
{
public:
//#if $header_only
    sample_class_t(std::string name)
        : m_name{ std::move( name ) }
    {}
//#else
    sample_class_t(std::string name);
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
// make_canonical_name()
//

inline std::string make_canonical_name(std::string_view name)
{
    constexpr char hex_digits[] = "0123456789ABCDEF";
    std::string result_name;
    result_name.reserve(name.size() + std::accumulate(begin(name), end(name), 0, [](auto memo, auto ch) {
                            return memo + (std::isprint(ch) ? 1 : 4);
                        }));

    for (const auto ch : name) {
        if (std::isprint(ch)) {
            result_name += ch;
        } else {
            const auto code = static_cast<std::uint8_t>(ch);
            result_name += '\\';
            result_name += 'x';
            result_name += hex_digits[code >> 4];
            result_name += hex_digits[code & 0x0F];
        }
    }

    return result_name;
}

}  // namespace details
//#end if

//
// make_canonical_sample()
//

/**
 * @brief Make canonical instance for a given name
 *
 * @return An instance of sample_class_t with caonical name.
 */
//#if $header_only
inline sample_class_t make_canonical_sample( std::string_view name )
{
    return sample_class_t{ details::make_canonical_name( name ) };
}
//#else
sample_class_t make_canonical_sample(std::string_view name);
//#end if

}  // namespace ${cpp_namespace_prefix}${name}

namespace fmt
{

template <>
struct formatter<${cpp_namespace_prefix}${name}::sample_class_t> {
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
    auto format(const ${cpp_namespace_prefix}${name}::sample_class_t& s, Format_Context& ctx) {
        return format_to(ctx.out(), "{{ {} }}", s.name());
    }
};

}  // namespace fmt
