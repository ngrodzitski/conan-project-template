#include <${src_path_prefix}${name}/impl/helpers.hpp>

#include <cctype>
#include <cstdint>
#include <numeric>

namespace ${cpp_namespace_prefix}${name}::impl
{

namespace /* anonymous */
{

constexpr char hex_digits[] = "0123456789ABCDEF";

}  // anonymous namespace

//
// make_canonical_name()
//

std::string make_canonical_name(std::string_view name)
{
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

}  // namespace ${cpp_namespace_prefix}${name}::impl
