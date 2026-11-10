# Cyber-Cop version provenance — archival reconstruction

Compiled from 66 README files and technical notes covering v0.1 through v36a. This is a **development and testing timeline**, not a list of every feature still active in the final build: some intermediary solutions were replaced or corrected. Early v0.1–v0.9 numbering later changed to v10–v36. MouseLab was a **separate experimental ROM line**: prototype behavior should not automatically be claimed as part of the main game until integrated in v35.

- Faster turning while standing and moving; the very first gameplay patch only changed angular-step constants. [v0.1]
- Prevented unwanted direction repeat in in-game menus; added six-button pad polling and Mode sleep/wake. XYZ were not yet assigned. [v0.2]
- Added A+Left/Right strafing and X/Z/Y item cycling/use; reverted the experimental reverse-turn inversion from v0.2. [v0.3]
- Disabled ordinary strafing during jumps, broadened hotkey contexts and tested vertical-striped wall shading in an experimental variant. [v0.4]
- Fixed hotkey context after inserting an ID card in a terminal and added a perspective-projected horizontal wall stripe. [v0.5]
- Lowered the wall stripe and added depth-sensitive tone; enabled XYZ in object panels and Start skipping of early logos/story. [v0.6]
- Added context-sensitive tap-A interaction on release and a 4×4 distance-based wall dithering pattern. [v0.7]
- Introduced optimized depth sorting without changing rendered frames or game logic. [v0.8]
- Optimized enlarged sprites using cached pixel pairs and transparency masks. [v0.9]
- Simplified ordinary-wall depth calculations and improved pointer-list sorting. [v10]
- Early rejection of ordinary wall cells fully occluded by continuous ordinary-wall segments; alternate dithering experiments. [v11]
- Selected 2×2 as the standard dithering pattern; skipped rasterizing fully offscreen projected surfaces and stripes. [v12]
- Expanded the ROM to 2 MiB for large-sprite/destruction rendering tables; fixed unnecessary theme restarts on Down+A. [v13]
- Reworked front-end options; added Sound Test, initial resource cheats, separate wall-effect switches, and alternating regional title logos. [v14]
- Adjusted character/equipment confirmation; enabled A/C in object panels, Repair focus after quick pickup of broken items and initial all-access option. [v15]
- Added Back and reorganized Options; made access level selectable 0–7, added an in-sleep settings menu and optimized one 2×2 dithering path. [v16]
- Fixed reproduced near-plane projection defects; restored the native sleep fade and introduced password-only SRAM persistence (not full world history). [v17]
- Separated Start New Game, Resume Saved Game and Enter Password; ID-card auto-selection now focuses Use. [v18]
- Added five selectable dithering modes (Off / 2×2 / 4×4 / 4×8 / Bar) and fixed held-button repeat on password entry. [v19]
- Adjusted sleep-menu arrow placement, dithering-option input and music transitions on leaving menus. [v20]
- Extended SRAM to character/inventory/injury, floor-item and terminal history; fixed lethal injury reconstruction and specific HUD/near-stripe corruption. [v21]
- Fixed No Saved Game presentation and selected music-sequence stopping behavior when the main theme is disabled. [v22]
- Added the mod version to the main menu and refined Music Off so lift, alarm and other environmental sequences still operate. [v23]
- Restored a precise first standing-turn step, then faster repeats; introduced low-energy warnings and Auto Sleep; corrected airlock Enter, bomb-hotkey panel entry and cursor lookup between panels. [v24]
- Restored original empty-battery blinking alongside the separate low-energy warning; enabled main music on SRAM Resume when appropriate. [v25]
- Major set: diagonal strafe, A-release movement gestures, VBlank input buffering, same-type consumable selection, Flying Lead, guarded Refill/Chemicals, item labels, bomb confirmation, grenades/Eye/fuse-box fixes, randomized codes preserved in SRAM, stereo gas correction and original project tiles/credits. [v26]
- Fixed unwanted camera rotation during diagonal strafing; refined item-label placement and mod credits. [v27]
- Added sleep on detectable controller disconnection; improved item-label colors under HUD/Visor changes and moved mod credits to the end. [v28]
- Refined transparent-background item labels and mod-credits placement; ensured main-theme playback at the ending. [v29]
- Suppressed labels during expanded elevator password display, refined centering and restored Music On after credits. [v30]
- Split Cheats into a main-menu entry and second sleep-menu page; prevented unloaded-tile flashes when early logos were skipped. [v31]
- Hid Cheats until four separate Downs on Options; fixed VDP/shadow state on logo skipping, suppressed labels on expanded sleep HUD, focused Use for lockpicks, held keypad warning while alarm blocks access and raised low-energy warning to 15%. [v32]
- Replaced the numeric sleep-gain readout with the native Energy bar; prioritized Gas Mask, blocked lockpicking during alarms, cleared stale Use after a lift trip and fixed Jet Pack/alarm audio ownership. [v33]
- Fixed Drop fallback, Scanman Screen/Use selection, outside lift buttons and the sleep Energy display; stopped menu wraparound, increased timeout and allowed a second Use to switch off Jet Pack. [v34]
## Experimental MouseLab line

- Initial separate Sega Mouse laboratory: port-2 protocol, polling-method comparisons and an isolated test world, not the main game. [MouseLab Test01]
- Prototyped captured-look/free-cursor modes, coordinate-based manual aiming, vertical view offset and sensitivity. [MouseLab Test02]
- Expanded vertical offset to ±100 pixels; refined HUD/panel hitboxes, in-sleep menus and held-button handling. [MouseLab Test03]
- Fixed Test03 VBlank-stack startup failure; prevented drag-in clicks and improved the sensitivity slider. [MouseLab Test04]
- Removed VBlank/mouse freezes and refined buttons, repair ownership, bomb confirmation and Scanman feedback. [MouseLab Test05–06]
- Refined captured/free mouse-button assignments, held-state graphics, flower-view rotation and panel interactions. [MouseLab Test07–08]
- Finalized experimental lift/Scanman panel and mouse interaction behavior; accepted changes became the basis for v35. [MouseLab Test09]
## Return to the main game

- Integrated Sega Mouse and selected MouseLab Test09 behavior into the main game, including an isolated test map. [v35]
- Fixed black-screen startup regression caused by mouse VBlank polling/Z80 interaction; refined click areas and graphical layout. [v35a]
- Start now launches the highlighted new-game submenu entry, including the hidden test map. [v35b]
- Fixed sensitivity-slider graphics and VRAM tile placement; mouse input is blocked during accepted elevator trips; free-cursor mode avoids unintended jump/crouch gestures. [v35c]
- First integrated the 16-floor Amiga Mission Disk campaign: distinct SRAM/passwords, new robot/sounds, objects, maps, ending and lights. [v36 test01]
- Corrected test-world map tables, Mission color bands and HUD restoration; added Holo. labels, Mission Scanman, second test map and initial memorial. [v36 test02]
- Refined memorial, sprites and chair debris; added mouse-driven front end, Lamps options and optimized ellipses; restored native lift speed. [v36 test03]
- Fixed memorial palette/scroll, lift persistence, access logic, barrel rendering and auto-aim prioritization; restricted unnecessary droid supplies. [v36 test04]
- Lowered both barrel sprites; improved wrong-direction lift calls, second-button feedback and shaded indicators. [v36 test05]
- Final cumulative build: extra dwell at the lift's extreme floor, preserved breakage of dropped items and the v36 menu label. The Kega cursor issue was not claimed as fixed. [v36]
- The `wip` hotfix restores lock/lift digit palettes, shades inserted-card indicators and renders the final destination floor before closing the call panel. [v36a]

## Separate research and claims to avoid

The supplied archive mentions a **custom Atari ST character disk** as a separate research topic (e.g. v33_QUESTIONS_RU.md and v34_DEVELOPMENT.md). **No documentation or implementation of a completed disk-image generator was present in these 66 text files**, so it is not listed as a Genesis ROM feature. The bilingual 32-map Atlas 40 is a separate companion tool ([documentation](../atlas39/README_RU.md)), not game-ROM functionality. The Kega cursor-jump report, all extreme near-plane artifacts and real-console compatibility have **not** been established as fixed.

The [English project README](../README.md) describes **current cumulative game features**; the [v36 release notes](../RELEASE_NOTES_v36_RU.md) and [v36a hotfix record](https://github.com/Valetos2/Cyber-Cop-Genesis-mod/blob/wip/v36/RELEASE_V36A_RU.md) provide additional technical detail.
