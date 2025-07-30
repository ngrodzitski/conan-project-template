#include <${names.src_path_prefix}/impl/helpers.hpp>

#include <cctype>
#include <cstdint>
#include <numeric>

namespace ${names.cpp_namespace}::impl
{

namespace /* anonymous */
{

constexpr char ${names.cpp_hex_digits_var}[] = "0123456789ABCDEF";

}  // anonymous namespace

//
// ${names.cpp_make_canonical_name_func}()
//

std::string ${names.cpp_make_canonical_name_func}( std::string_view name )
{
    std::string result;
    result.reserve( name.size() + std::accumulate(begin(name),
                    end(name),
                    0,
                    [](auto memo, auto ch) {
                        return memo + (std::isprint(ch) ? 1 : 4);
                    } ) );

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

}  // namespace ${names.cpp_namespace}::impl
