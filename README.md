<div align="center">

  [![PRAL333 logo][pral333-logo]][website-link]

  <h3>PRAL333</h3>

  A UCI chess engine with an ultra-aggressive style.
  <br>
  <strong>[Explore PRAL333 docs »][readme-link]</strong>
  <br>
  <br>
  [Report bug][issue-link]
  ·
  [Open a discussion][discussions-link]
  ·
  [Discord][discord-link]
  ·
  [Blog][website-blog-link]

  [![Build][build-badge]][build-link]
  [![License][license-badge]][license-link]
  <br>
  [![Release][release-badge]][release-link]
  [![Commits][commits-badge]][commits-link]
  <br>
  [![Website][website-badge]][website-link]
  [![Fishtest][fishtest-badge]][fishtest-link]
  [![Discord][discord-badge]][discord-link]

</div>

## Overview

[PRAL333][website-link] is a **UCI chess engine** that analyzes chess positions
and computes the optimal moves with an aggressive style profile.

PRAL333 **does not include a graphical user interface** (GUI) that is required
to display a chessboard and to make it easy to input moves. These GUIs are
developed independently and are available online. **Read the documentation for
your GUI** of choice for information about how to use PRAL333 with it.

See also the PRAL333 [documentation][readme-link] for further usage help.

## Files

This distribution of PRAL333 consists of the following files:

  * [README.md][readme-link], the file you are currently reading.

  * [Copying.txt][license-link], a text file containing the GNU General Public
    License version 3.

  * [AUTHORS][authors-link], a text file with the list of authors for the project.

  * [src][src-link], a subdirectory containing the full source code, including a
    Makefile that can be used to compile PRAL333 on Unix-like systems.

  * a file with the .nnue extension, storing the neural network for the NNUE
    evaluation. Binary distributions will have this file embedded.

## Contributing

__See [Contributing Guide](CONTRIBUTING.md).__

### Donating hardware

Improving PRAL333 requires a massive amount of testing. You can donate your
hardware resources by installing the [Fishtest Worker][worker-link] and viewing
the current tests on [Fishtest][fishtest-link].

### Improving the code

In the [chessprogramming wiki][programming-link], many techniques used in
PRAL333 are explained with a lot of background information.
The main chess programming references describe many features and techniques
used by modern engines. However, they are generic rather than focused on
PRAL333's precise implementation.

The engine testing is done on [Fishtest][fishtest-link].
If you want to help improve PRAL333, please read this [guideline][guideline-link]
first, where the basics of chess engine development are explained.

Discussions about PRAL333 take place mainly in the PRAL333
[Discord server][discord-link]. This is also the best place to ask questions
about the codebase and how to improve it.

## Compiling PRAL333

PRAL333 has support for 32 or 64-bit CPUs, certain hardware instructions,
big-endian machines such as Power PC, and other platforms.

On Unix-like systems, it should be easy to compile PRAL333 directly from the
source code with the included Makefile in the folder `src`. In general, it is
recommended to run `make help` to see a list of make targets with corresponding
descriptions. An example suitable for most Intel and AMD chips:

```
cd src
make -j profile-build
```

Detailed compilation instructions for all platforms can be found in our
[documentation][wiki-compile-link]. Our wiki also has information about
the [UCI commands][wiki-uci-link] supported by PRAL333.

## Terms of use

PRAL333 is free and distributed under the
[**GNU General Public License version 3**][license-link] (GPL v3). Essentially,
this means you are free to do almost exactly what you want with the program,
including distributing it among your friends, making it available for download
from your website, selling it (either by itself or as part of some bigger
software package), or using it as the starting point for a software project of
your own.

The only real limitation is that whenever you distribute PRAL333 in some way,
you MUST always include the license and the full source code (or a pointer to
where the source code can be found) to generate the exact binary you are
distributing. If you make any changes to the source code, these changes must
also be made available under GPL v3.

## Acknowledgements

PRAL333 uses neural networks trained on [data provided by the Leela Chess Zero
project][lc0-data-link], which is made available under the [Open Database License][odbl-link] (ODbL).


[authors-link]:       https://github.com/Falthera/Pral333/blob/main/AUTHORS
[build-link]:         https://github.com/Falthera/Pral333/actions/workflows/pral333-release.yml
[commits-link]:       https://github.com/Falthera/Pral333/commits/main
[discord-link]:       https://discord.gg/GWDRS3kU6R
[issue-link]:         https://github.com/Falthera/Pral333/issues/new/choose
[discussions-link]:   https://github.com/Falthera/Pral333/discussions/new
[fishtest-link]:      https://github.com/Falthera/Pral333/actions
[guideline-link]:     https://github.com/Falthera/Pral333/blob/main/CONTRIBUTING.md
[license-link]:       https://github.com/Falthera/Pral333/blob/main/Copying.txt
[programming-link]:   https://www.chessprogramming.org/Main_Page
[readme-link]:        https://github.com/Falthera/Pral333/blob/main/README.md
[release-link]:       https://github.com/Falthera/Pral333/releases/latest
[src-link]:           https://github.com/Falthera/Pral333/tree/main/src
[pral333-logo]:       prallogo.png
[uci-link]:           https://backscattering.de/chess/uci/
[website-link]:       https://github.com/Falthera/Pral333
[website-blog-link]:  https://github.com/Falthera/Pral333/releases
[wiki-link]:          https://github.com/Falthera/Pral333/blob/main/README.md
[wiki-compile-link]:  https://github.com/Falthera/Pral333/blob/main/README.md#compiling-pral333
[wiki-uci-link]:      https://github.com/Falthera/Pral333/blob/main/README.md#overview
[wiki-usage-link]:    https://github.com/Falthera/Pral333/blob/main/README.md#overview
[worker-link]:        https://github.com/Falthera/Pral333/actions
[lc0-data-link]:      https://storage.lczero.org/files/training_data
[odbl-link]:          https://opendatacommons.org/licenses/odbl/odbl-10.txt

[build-badge]:        https://img.shields.io/github/actions/workflow/status/Falthera/Pral333/pral333-release.yml?branch=main&style=for-the-badge&label=pral333&logo=github
[commits-badge]:      https://img.shields.io/github/commits-since/Falthera/Pral333/latest?style=for-the-badge
[discord-badge]:      https://img.shields.io/discord/435943710472011776?style=for-the-badge&label=discord&logo=Discord
[fishtest-badge]:     https://img.shields.io/website?style=for-the-badge&down_color=red&down_message=Offline&label=PRAL333&up_color=success&up_message=Online&url=https%3A%2F%2Fgithub.com%2FFalthera%2FPral333
[license-badge]:      https://img.shields.io/github/license/Falthera/Pral333?style=for-the-badge&label=license&color=success
[release-badge]:      https://img.shields.io/github/v/release/Falthera/Pral333?style=for-the-badge&label=pral333%20release
[website-badge]:      https://img.shields.io/website?style=for-the-badge&down_color=red&down_message=Offline&label=pral333&up_color=success&up_message=Online&url=https%3A%2F%2Fgithub.com%2FFalthera%2FPral333
