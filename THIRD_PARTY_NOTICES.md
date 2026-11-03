# Third-party notices

The release zip contains a modified build of Nookery (Nookery.exe) and two libraries it was built against (libpng16.dll and zlib1.dll). Nookery.exe includes the components below. Each licence is reproduced in full in the licenses folder, which ships in the release zip too.

No Nintendo game data is included anywhere. Nookery's PC build compiles every game texture, model and sound as an empty buffer and fills it at runtime from the player's own disc image.

## Nookery and the code it is built on

| Component | Authors | Licence | Licence file |
|---|---|---|---|
| [Nookery](https://github.com/flyngmt/ACGC-PC-Port), the PC port layer, including its kyureki calendar library | FlyingMeta and contributors | MIT | licenses/nookery.txt, licenses/kyureki.txt |
| [ac-decomp](https://github.com/ACreTeam/ac-decomp), the Animal Crossing decompilation Nookery is built on | ACreTeam | CC0 1.0 (public domain) | licenses/nookery.txt |
| [FixNES](https://github.com/FIX94/fixNES), the NES emulator inside Nookery | FIX94 | MIT | licenses/fixnes.txt |
| [Aurora](https://github.com/encounter/aurora), the GameCube platform layer | Luke Street (encounter) and contributors | MIT | licenses/aurora.txt |
| [Borealis](https://github.com/encounter/borealis), the app framework | Luke Street (encounter) and contributors | MIT | licenses/borealis.txt |

## Libraries

| Library | Authors | Licence | Licence file |
|---|---|---|---|
| [RmlUi](https://github.com/mikke89/RmlUi) | CodePoint Ltd, Shift Technology Ltd, and contributors | MIT | licenses/rmlui.txt |
| [Dear ImGui](https://github.com/ocornut/imgui) | Omar Cornut | MIT | licenses/imgui.txt |
| [FreeType](https://freetype.org) | The FreeType Project | FreeType Licence | licenses/freetype-ftl.txt |
| [{fmt}](https://github.com/fmtlib/fmt) | Victor Zverovich and contributors | MIT | licenses/fmt.txt |
| [JSON for Modern C++](https://github.com/nlohmann/json) | Niels Lohmann | MIT | licenses/nlohmann-json.txt |
| [cxxopts](https://github.com/jarro2783/cxxopts) | Jarryd Beck | MIT | licenses/cxxopts.txt |
| [Abseil](https://github.com/abseil/abseil-cpp) | The Abseil Authors | Apache 2.0 | licenses/abseil.txt |
| [xxHash](https://github.com/Cyan4973/xxHash) | Yann Collet | BSD 2-Clause | licenses/xxhash.txt |
| [Zstandard](https://github.com/facebook/zstd) | Meta Platforms, Inc. and affiliates | BSD 3-Clause | licenses/zstd.txt |
| [Tracy](https://github.com/wolfpld/tracy) (client library, profiling switched off) | Bartosz Taudul and contributors | BSD 3-Clause | licenses/tracy.txt |
| [SQLite](https://sqlite.org) | D. Richard Hipp and contributors | Public domain | none needed |
| [libpng](http://www.libpng.org/pub/png/libpng.html) (libpng16.dll) | The PNG Reference Library Authors | libpng licence | licenses/libpng.txt |
| [zlib](https://zlib.net) (zlib1.dll) | Jean-loup Gailly and Mark Adler | zlib licence | licenses/zlib.txt |

Portions of this software are copyright 2026 The FreeType Project (www.freetype.org). All rights reserved.

Nookery also loads SDL3, Dawn (WebGPU) and nod as separate DLLs. Those come with Nookery itself and are not part of this release.
