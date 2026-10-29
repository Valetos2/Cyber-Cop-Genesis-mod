# Development and building

## Current version: v35c

The current published patch is **v35c**. The offline map viewer is **Atlas r37**; atlas revisions are separate from game build versions.

To build v35c, use Python 3 (the builder itself only requires the standard library):

```sh
python3 sources/build_v35.py /path/to/Cyber-Cop.bin /path/to/Corporation.bin build/v35c
```

Both inputs must be your own correct original, uncompressed ROMs. The build scripts verify their SHA-256 values:

- Cyber-Cop: `98838ed8d69349ab64a99e4a4e0ea72843d47b175b69fda36957283932f0aba9`
- Corporation: `226368b1693af2db21bb1cc640b94d5b021c9ff20fcb86207d2b76590503cc98`

The build reconstructs v34, applies the MouseLab Direct integration and v35c changes, and generates a BIN, IPS patch and symbol JSON. The patched ROM is a **local output, not a project distribution file**.

Expected v35c ROM SHA-256: `fc4ac6984e0499d5bfbf7c18df0c3a153e077c9f67973b57edb1981b14b2fde4`.

See [detailed build notes](sources/BUILD_RU.md), [release notes](RELEASE_NOTES_v35c.md) and [test results](docs/v35c_TEST_RESULTS.txt).

**Precomputed source inputs:** `sources/v35/boot_vram.bin` is a VRAM snapshot used by the current build process; `sources/v34/easter_tiles.bin` contains custom tiles. The VRAM snapshot may incorporate original game graphics; the project's Apache 2.0 license does **not** grant rights to third-party material within any generated data. A self-contained ROM-driven asset extractor is a possible future improvement.

## Historical builds and research

Older build scripts remain in `v13/`, `v33/` and `v34/` to preserve the development history. The previous v34 build is:

```sh
python3 v34/build_v34.py /path/to/Cyber-Cop.bin /path/to/Corporation.bin build/v34
```

Some earlier test scripts require original ROMs, intermediate historical builds, Fusion GST snapshots or local fixtures not shipped in this repository. Testing under Unicorn/Capstone/Pillow is a targeted research technique, not a substitute for complete playthrough testing or real hardware verification.

## Offline atlas r37

The finished bilingual viewer is at `atlas/Cyber-Cop_Atlas.html` and `atlas/Cyber-Cop_Atlas_en.html`. Both files need to remain together for language switching. It works locally without a web server or remote asset downloads.

The `atlas/` folder also includes map PNGs, extracted `data.json`, `cells.csv`, documentation and existing research scripts. The `atlas35/` directory holds older research/rendering tools, which may still depend on original ROMs and save states.

**Rights note:** HTML embeds game imagery, and PNG/JSON/CSV outputs contain material extracted from the original game. These resources are acknowledged for their original copyright owners; they are **not** relicensed under Apache 2.0. Publishing them does not establish that redistribution rights have been cleared.

A future alternative would import a user-provided ROM and extract visual resources locally in the browser.

## Repository policy

- **Never commit original or fully modified commercial ROM files.**
- Release approved standalone IPS patch files in `patches/` and script/tool sources in `sources/`.
- Include supporting documentation and tests, with limitations stated clearly.
- The atlas and its data are kept separately under `atlas/` from the game patch.
- Historic files and experiments should not be deleted merely because they are absent from later update packages.
- Keep user-supplied save data, credentials, emulator states, full ROMs and temporary builds out of commits.

See [CONTRIBUTING.md](CONTRIBUTING.md), [NOTICE](NOTICE), and [ORIGINAL_GAME_CREDITS.md](ORIGINAL_GAME_CREDITS.md).
