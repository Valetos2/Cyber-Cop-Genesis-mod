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
