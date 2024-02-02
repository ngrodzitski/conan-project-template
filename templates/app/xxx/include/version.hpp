// clang-format off
#pragma once

//#if "corporate_tag_normalized_word" in self.keys()
//#set $macro_prefix = $corporate_tag_normalized_word.upper() + "_" + $name.upper()
//#else
//#set $macro_prefix = $name.upper()
//#end if
#define ${macro_prefix}_VERSION_CODE( major, minor, patch ) \
    ( ( ( major ) << 16UL ) + ( ( minor ) << 8UL ) + ( ( patch ) << 0UL ))

#define ${macro_prefix}_VERSION_MAJOR 0ull
#define ${macro_prefix}_VERSION_MINOR 1ull
#define ${macro_prefix}_VERSION_PATCH 0ull

// Consider to insert real revision here on CI:
#define ${macro_prefix}_VCS_REVISION "n/a"

#define ${macro_prefix}_VERSION \
    ${macro_prefix}_VERSION_CODE( ${macro_prefix}_VERSION_MAJOR, ${macro_prefix}_VERSION_MINOR, ${macro_prefix}_VERSION_PATCH )

