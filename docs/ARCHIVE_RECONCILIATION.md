# Release archive reconciliation — 2026-11-11

Compared supplied v35c, v36 and v36a ZIP packages, plus the Atlas r37 publication archive. The following checks were performed locally on the user-supplied files:

- The IPS labeled v35c_to_v36 reproduces the packaged v36 ROM byte for byte when applied to the exact packaged v35c ROM.
- The IPS labeled v36_to_v36a reproduces the packaged v36a ROM byte for byte when applied to the exact packaged v36 ROM.
- v36 SHA-256: 8f585c6218d8f193a01478f8bbe6d7c40406d1c53ecf9a4bbe01da96d5faf43b
- v36a SHA-256: 0c60ac5b22650f704dcc90eeea59a32be39eb6d56f69a918dce7f7925237ec41
- Incremental IPS SHA-256: 8da904414ccc0e6f6b80517ce980e88113e4926d81c8d709edb1baa1f8028f87

Published in main: the small, validated incremental v36-to-v36a IPS and selected **source-only** Mission Disk and v36 inspection scripts absent from the repository. Do not confuse an incremental IPS with one intended for the original Cyber-Cop ROM.

The supplied v36 archive also includes original DOS data (CORPRTNC.DAT), Amiga and Atari game resources, emulator save states, PCM samples and generated game imagery. **Those binaries were deliberately not committed.** In a reorganized private archive, the DOS data file was moved from rebuild/next/dos/corporation/corporation/CORPRTNC.DAT to rebuild/next/dos/CORPRTNC.DAT. Existing analysis scripts search recursively within next/dos, so their expected search root remains the same.

The new source scripts reference user-provided ROMs, research files, emulator states or local emulator executables that are not in GitHub. Validating syntax and archive/patch integrity does not replace a complete source rebuild or game playthrough.


## Atlas 40 standalone package and cleanup

The user-provided standalone Atlas 40 ZIP passed CRC validation: two self-contained HTML files, README, JSON, CSV, and 984 PNG exports. This package remains separate from GitHub source.

Retained: `atlas39/` (current Atlas 40 generator) and `atlas37/` (required template, sprite tool and generator inputs). Removed from current HEAD: old generated Atlas r37 outputs and legacy research scripts under `atlas/` plus redundant sources in `atlas35/` and `atlas38/`. Everything remains recoverable in Git history at commit `1edde6660f9962bf161f645d7b2da42eb98d16c2`. Updated r37 tests to read locally regenerated files in `atlas37/`. Preserved `Cyber-Cop_v34_Wall_Comparison.png` and `checks/v35c/*.png`. No commercial game assets or complete Atlas ZIP were uploaded to GitHub in this cleanup. Full rebuilding still requires private ROM and research input files.
