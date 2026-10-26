# Building v34

Python 3 is sufficient for the ROM builder. Run from a checkout:

```sh
python3 v34/build_v34.py /path/to/Cyber-Cop.bin /path/to/Corporation.bin build/v34
```

Both original ROM hashes are checked. See README for their SHA-256 values. Expected output ROM SHA-256:

`3d8de656abcea8684ffd616812b173b28dfac7522b1953f974a4befa66e2e846`

The builder generates BIN, cumulative IPS and symbol metadata. Sprite acceleration tables are generated from the supplied ROM; pre-extracted game sprite data is not checked in. `v34/easter_tiles.hex` contains the contributor's custom Easter-egg artwork, not a complete ROM. The older `v13` modules are active build dependencies, not separate downloads users must patch in sequence.

## Tests and atlas research scripts

The recorded test results execute selected M68000 routines under Unicorn, with hardware-facing operations stubbed or recorded. They are not a full console emulator, a YM2612 listening test or a guarantee of physical-cartridge compatibility.

Research tests in `v34/` currently refer to local historical ROM builds and user-provided Fusion GST fixtures under `upload/`. These inputs are deliberately excluded. Install `unicorn`, `capstone`, `Pillow` for CPU/image analysis. The tests are supplied as research material, not advertised as a one-command clean-checkout CI suite.

Likewise, `atlas35/` contains the template, rendering scripts, translation and JavaScript tests. Its existing rendering workflow expects historical v29/v30 builds, map data extracted by native routines and local GST-backed initialization. Generated data.json/images.json/HTML/PNG resources are not included. The offline atlas archive contains these generated outputs for private use. A portable extractor and browser-side ROM import are future work; opening template.html alone is not a working atlas.

A future public viewer should load a local ROM through a file picker and extract maps as well as graphics in the browser, without uploading the ROM. Original assets must not be hidden in JSON/base64 or committed as generated fallback content. This architecture reduces redistributed game content; it is not a blanket legal clearance.

## Continuing development

Keep source and documentation changes on the existing `main` branch as requested by the project owner. Keep original/patched ROMs, IPS, SRAM/GST and generated asset bundles out of commits; distribute testing packages separately. Fetch the branch head and preserve user edits before updating it.

Mission Disk belongs to the Amiga version. The Atari ST personalized-character disk is a separate feature for future investigation. Sega Mouse support and additional Amiga levels are not in v34. Their source images and intended mouse button mapping still need to be provided and examined.

