# Cyber-Cop / Corporation — v35c Release Notes

**Sega Genesis / Mega Drive improvement patch — 29 October 2026**

This release supersedes the earlier v34 development build and integrates the accepted Sega Mouse / MouseLab improvements into the main game. **Atlas revision 37 is a separate, standalone offline level viewer; its revision number does not match the ROM version.**

## Highlights

- **Sega Mouse (controller port 2):** free cursor and captured-look modes, mouse aiming, interactions with panels, inventory and sleep menu, adjustable sensitivity, and vertical view offset. Joystick controls remain available.
- **Input and UI fixes:** improved hitboxes for panel controls, press-and-hold feedback without repeated clicks, fixes to the Options sensitivity slider graphics, and protection against accidental inputs.
- **Elevator safety:** following selection of a valid floor, all mouse movement and clicks are blocked until the elevator reaches it; held input must be released before the next click is accepted.
- **Gameplay and presentation:** test-world access, revised bomb confirmation indication, Scanman brightness-button feedback, and many fixes carried over from v34.
- **Reliability:** corrected a VBlank/Z80 interaction that previously caused a black-screen startup regression; transient settings reset without deleting SRAM.

Some researched changes, including punch damage to environmental objects and mouse clicks in the character/equipment creation menus, **are not included** in v35c. See [research notes](docs/v35c_RESEARCH_RU.md) for details.

## Applying the patch

1. Obtain the correct, **unmodified, uncompressed** original **Cyber-Cop** ROM in BIN format. The repository does not distribute game ROMs.
2. Verify that its SHA-256 is:
   `98838ed8d69349ab64a99e4a4e0ea72843d47b175b69fda36957283932f0aba9`
3. Apply [`Cyber-Cop_v35c.ips`](patches/Cyber-Cop_v35c.ips) to that original ROM using an IPS-compatible patching tool.
4. **Do not apply it over a previously patched v34 or MouseLab ROM.** Keep an untouched original backup.
5. Test the output in a compatible emulator. Always back up SRAM and start via reset/new game/password/resume rather than importing an older emulator save state.

Expected patched ROM SHA-256:

`fc4ac6984e0499d5bfbf7c18df0c3a153e077c9f67973b57edb1981b14b2fde4`

Patch SHA-256:

`6538be2cd79fbfa9e002d546250eb7615f7c52a7e551068eca358bb82d8385ae`

## Source and testing

- [Build from two original ROMs](sources/BUILD_RU.md) — Python 3, standard library for the build itself. The additional original **Corporation** ROM is required for building, but **not** for applying the ready-made IPS.
- [Full Russian fix list](docs/Cyber-Cop_v35c_Fixes_RU.md)
- [v35c notes (Russian)](docs/v35c_README_RU.md)
- [Recorded test results](docs/v35c_TEST_RESULTS.txt)
- [Research and deferred improvements](docs/v35c_RESEARCH_RU.md)

The packaged build was tested using targeted CPU/UI tests and a BlastEm 1.0.0 startup run. It has **not** been represented as a complete playthrough or a guarantee of compatibility with every emulator and real console.

## Atlas r37

The separate [offline atlas](atlas/README_EN.md) covers **16 floors**, with clickable cells, map legend, resource previews, English and Russian user interfaces, and viewer-state preservation when switching languages.

Download both [`Cyber-Cop_Atlas.html`](atlas/Cyber-Cop_Atlas.html) and [`Cyber-Cop_Atlas_en.html`](atlas/Cyber-Cop_Atlas_en.html) into the same folder before opening them locally. Embedded images mean no network access is required. The [atlas source data](atlas/data.json) and [cell table](atlas/cells.csv) are also provided.

## Copyright and attribution

The IPS patch is an unofficial fan modification. Original Corporation / Cyber-Cop game graphics, level information, sound and other material remain subject to the respective owners' rights. The atlas contains extracted game resources; its inclusion does not imply those resources are available under Apache License 2.0.

Project contributions: Valentin **"Valet2"** Kozin, with AI-assisted technical development using GPT-6 Astra. See [CREDITS.md](CREDITS.md), [NOTICE](NOTICE) and [LICENSE](LICENSE).
