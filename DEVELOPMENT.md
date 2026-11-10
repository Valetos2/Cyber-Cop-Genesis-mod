# Development and building

## Source milestones and published patch

The **`main` source tree contains v36a** (the completed hotfix on top of the two-campaign, 4 MiB v36 ROM). The `wip` branch was merged via [PR #2](https://github.com/Valetos2/Cyber-Cop-Genesis-mod/pull/2). The latest **standalone IPS for the original base ROM** under `patches/` is v35c. An additional [incremental v36 → v36a IPS](patches/v36_to_v36a.ips) is included and is valid only for the exact v36 base (SHA-256 `8f585c6218d8f193a01478f8bbe6d7c40406d1c53ecf9a4bbe01da96d5faf43b`). Game sources, independently supplied release packages and binary patches are different publication artifacts; having the source code in GitHub does not imply the completed commercial-ROM output can be downloaded here. See [English project overview](README.md), [Russian cumulative overview](README_RU.md), [v36 release notes](RELEASE_NOTES_v36_RU.md) and [v36a hotfix notes](v36/RELEASE_V36A_RU.md).

### Historical reproducible v35c builder

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

## Why older source directories are retained

A source-dependency review was done when v36a was merged into `main`:

- `sources/build_v35.py` rebuilds v35c using **`sources/v13/` → `sources/v34/` → `sources/mouse_lab/` → `sources/v35/`** in that order. These are build dependencies, not redundant leftovers.
- `v36/build.py` starts from a locally produced **`v35c/Cyber-Cop_v35c.bin`**, loads **`v35c/symbols.json`** and **`v34/symbols.json`**, and uses scripts/data from **`mission_port36/`**, **`amiga_research/`** and **`v36/`**. The prebuilt v35c BIN is intentionally not committed: build and runtime tests depending on it cannot be performed from a pristine source checkout alone.
- `atlas39/` (the source for Atlas 40) also reads files produced by **`atlas37/`** and the v36 ROM research/build environment. A directory's older number therefore does **not** prove it is safe to remove.
- Root `v13/`, `v33/`, earlier atlas revisions and historical tests preserve alternative build/test paths and reverse-engineering evidence. Some are not on the latest build path, but that is **not sufficient justification for deleting archival research**.

No historical directories were removed **during** the v36a merge. A later focused Atlas cleanup removed obsolete Atlas outputs and the no-longer-referenced `atlas35/` and `atlas38/` trees, retaining `atlas37/` because it is used by `atlas39/`. All removed material remains recoverable from Git history; game build directories were not changed.

## Historical builds and research

Older build scripts remain in `v13/`, `v33/` and `v34/` to preserve the development history. The previous v34 build is:

```sh
python3 v34/build_v34.py /path/to/Cyber-Cop.bin /path/to/Corporation.bin build/v34
```

Some earlier test scripts require original ROMs, intermediate historical builds, Fusion GST snapshots or local fixtures not shipped in this repository. Testing under Unicorn/Capstone/Pillow is a targeted research technique, not a substitute for complete playthrough testing or real hardware verification.

## Offline atlas: current Atlas 40 and historical r37

**Atlas 40** adds both campaigns (32 maps), bilingual UI, preserved view settings and richer map markers. Its source tools and [current Russian documentation](atlas39/README_RU.md) are retained under `atlas39/`; fully generated HTML/image packages are separate from source-only files. The directory name is historical and the documented package is Atlas 40.

Retained `atlas37/` scripts are required by the Atlas 40 generator in `atlas39/`. Old generated r37 HTML, map images, CSV and JSON under `atlas/`, and superseded `atlas35/` and `atlas38/` source trees, were removed from the current branch. Their contents can still be recovered from Git history. Atlas revisions are independent of game versions.

**Rights note:** HTML embeds game imagery, and PNG/JSON/CSV outputs contain material extracted from the original game. These resources are acknowledged for their original copyright owners; they are **not** relicensed under Apache 2.0. Publishing them does not establish that redistribution rights have been cleared.

A future alternative would import a user-provided ROM and extract visual resources locally in the browser.

## Repository policy

- **Never commit original or fully modified commercial ROM files.**
- Release approved standalone IPS patch files in `patches/` and script/tool sources in `sources/`.
- Include supporting documentation and tests, with limitations stated clearly.
- Store current Atlas 40 builder sources under `atlas39/` and its required legacy generator sources under `atlas37/`. Distribute fully generated image-containing Atlas packages separately.
- Historic files and experiments should not be deleted merely because they are absent from later update packages.
- Keep user-supplied save data, credentials, emulator states, full ROMs and temporary builds out of commits.

See [CONTRIBUTING.md](CONTRIBUTING.md), [NOTICE](NOTICE), and [ORIGINAL_GAME_CREDITS.md](ORIGINAL_GAME_CREDITS.md).
