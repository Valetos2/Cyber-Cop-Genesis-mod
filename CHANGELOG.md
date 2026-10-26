# Changes from the original Genesis game — v33

This is a cumulative description of the current modification, not a list of every experimental build. Superseded implementations are omitted. A few changes alter the original design deliberately; they are identified below. Atari ST, Amiga and DOS versions are not modified by this patch.

## Controls and input

- Increased turning speed both while stationary and while moving. A new stationary Left/Right press takes the original small angular step; further held steps use the increased step. Releasing, reversing direction or moving resets the fine-step state.
- Kept the established backward-turn direction after testing an alternative scheme.
- Added six-button pad detection and X/Z backpack cycling, Y item use and Mode sleep/wake. Shortcuts work without moving the inventory cursor onto the corresponding icon, including while an object interface is open; sleep blocks normal item shortcuts.
- Added contextual A pickup/interaction from the world, using the existing available-action checks. Directional A combinations retain movement semantics rather than accidentally picking up an object.
- Added A+Left/Right strafing, with forward/backward diagonal movement using one movement speed rather than summing two full-speed axes. Normal jumping blocks strafe; the existing sustained flight states can use it.
- Jump/crouch gestures use A release in the current movement scheme. A gesture already used for strafe does not trigger a jump or crouch when released. Camera heading remains stable during strafe and diagonal movement.
- Removed unwanted directional menu auto-repeat while preserving continuous world movement and held repair actions.
- Added VBlank sampling and a one-event-per-button pending mask for discrete actions, reducing lost short presses during slow frames. B, C, Start and six-button actions are covered; contextual inventory/panel inputs are handled separately. World movement and A movement gestures are not queued. Repeated presses of the same button before consumption merge into one event.
- A and C also activate selected controls on additional object/item panels. The main inventory icon strip retains its own controls.
- Detect loss of a previously present standard pad using the existing reads; after six missing samples, request native sleep at a safe world-loop point. Reconnection does not automatically wake the player. Receivers that continue answering as a pad cannot expose a wireless-controller disconnect.

## Inventory and object interfaces

- Preserve a usable item of the same type after consuming one of several copies. If none remain, select the next surviving item to the right in the previous inventory order.
- When Use becomes unavailable, move the icon-strip cursor left toward backpack cycling instead of wrapping right to Sleep.
- Correct hotkey entry into item panels, notably the timer bomb, so the interface receives the native cursor/control state.
- After quick pickup of a broken item, the next inventory opening focuses Repair if the selected item has not changed. Repair still requires the original held action.
- Successful automatic ID-card selection focuses Use. Successful lockpick selection on the door keypad does too; if no lockpick exists, the selection is left alone.
- After inserting the ID card in a terminal, select the flying lead once if it is present. Subsequent manual cycling remains possible.
- Prevent standalone consumption of Refill and Chemicals outside their Drink and Medi Kit refill contexts.
- Correct the world-item preview path where the special backpack slot could clear the object image. This is a verified shared-handler defect; it is not a claim that every possible missing Narcotics image was independently reproduced.
- Remove the unwanted extra graphic associated with the dropped embryo preview, without changing unrelated object graphics.
- Add a temporary native item-name label in the HUD. Its light HUD palette stays readable through normal Visor/light changes; the original HUD background is retained beneath the letters. Centering accounts for odd/even lengths. The label disappears after 100 VBlanks.
- Suppress this label in sleep and the elevator's expanded password display, and clear the earlier label before the sleep HUD expands.
- On the airlock keypad, Right from Enter goes directly to the yellow action button; Left from that button still returns to 6.
- The timer bomb's Enter confirms the entered time. Editing a digit cancels confirmation; activation requires confirmation. Closing an unactivated bomb leaves it unarmed, and reopening allows editing again.
- Door-keypad errors flash the right red lamp. While the alarm blocks the keypad, that lamp remains red and clears when the blocking alarm ends.

## Graphics and rendering

- Add distance-dependent screen-space wall dithering, defaulting to 2×2. Choices are Off, 2×2, 4×4, 4×8 and vertical bars, selected with Left/Right without wraparound. These are not perspective-mapped textures.
- Add a horizontal reference stripe below wall center, with depth-dependent tone and an independent On/Off option. Turning it off restores shading over the complete wall area.
- Correct stripe projection/clipping near the camera, including the reported close-wall block/flash cases. This does not mean all original near-plane artifacts have been eliminated.
- Reduce redundant work in scene sorting, wall filling and selected sprite-scaling loops.
- Add conservative early rejection of ordinary wall cells fully behind a continuous ordinary-wall segment. Doors, enemies and special Visor surfaces are not treated as interchangeable opaque walls. This is not a full visibility engine or a replacement raycaster.
- Avoid a second full wall fill for the reference stripe; draw the stripe over the wall that is already being rendered.
- Accelerate enlarged large sprites and destruction animations through optimized pixel-pair handling and build-time tables for the covered frames. Original nearest-neighbor source sampling and transparency remain; these tables are not mipmaps or filtered resized images.
- Keep the original draw-distance limit. Performance gains depend on the scene, and difficult directions on complex floors can still be slow.

## Energy, sleep and optional cheats

- Add deep periodic world-window dimming at or below 15% energy. Preserve the original empty-battery effect and place the energy warning in its separate timing window. These timings follow game updates, not guaranteed wall-clock seconds.
- Add optional Auto Sleep, off by default, at the final energy division. It uses the native sleep transition; waking remains manual. It is not invulnerability or a treatment for existing injuries.
- Restore full native black sleep fade, hide the crosshair, and enter inventory with the Sleep icon selected when sleep starts through Mode or the added automatic paths.
- A/B/C during sleep opens a settings page; moving beyond its ends reaches a second page of five cheats. Reopening starts on the settings page. Five seconds without input returns to dots; Mode/Start wakes the player.
- Update the native Energy bar during sleep every 25 PAL / 30 NTSC VBlanks when its value changes. The native wake routine credits the previewed gain once; no numeric overlay or glyph cache is used.
- Optional Infinite Energy blocks covered energy expenditure; Infinite Battery covers device battery and weapon charge paths; Invincibility bypasses new body-part damage, without healing existing damage. Access Level selects the real level 0–7, not an elevator-check bypass. Auto Sleep is the fifth entry.
- Cheat flags are not added to SRAM. The real access value, like other character progression, can be part of a checkpoint.

## Front-end menus and presentation

- Main menu: Start New Game, Resume Saved Game, Enter Password, Options; Cheats is initially hidden.
- At Options, four separate Down presses reveal Cheats and select it. Any other button resets the count; holding Down is not four presses. Hidden navigation stops at the ends; after unlocking it wraps. Unlock state lasts until a new gameplay session starts and is not stored in SRAM.
- Start New Game contains Default Character, Select New Character and Back. Options contains Music, Sound FX, Sound Test, Wall Dithering, Wall Stripe and Exit. Cheats has its five settings and Exit.
- Regular confirmation accepts A/B/C/Start. Exceptions: agent selection accepts A/B/C and ignores Start; equipment purchase uses A/B/C to buy and Start to launch; password Start submits the entered password. Options/Cheats Start selects Exit and performs the normal fade.
- On/Off settings accept action buttons and Left/Right; dithering and access level use arrows only. Access and dithering lists do not wrap.
- Preserve the selected main-menu row when returning from password entry and submenus. Prevent held entry buttons from typing repeated password letters. Clear the previous expanded menu when opening the password panel.
- Show No Saved Game in the existing main-menu message area when no valid SRAM checkpoint is available. This is an overlay, not a broken extra submenu.
- Allow Start to skip the early publisher/developer logos. During the transition, keep display output disabled both in the VDP register and its RAM shadow until resource loading is complete.
- Allow A/C as well as B/Start to skip the scrolling story.
- Alternate the Cyber-Cop and Corporation title graphics/palettes on successive title visits.
- Display the current version at the bottom right of the main menu, allowing three-digit version numbers.
- Append the romhack attribution after the original credits, before their trailing blank lines. Keep the original font, appropriate indentation and end-of-text-controlled scrolling duration.
- Preserve the user's restored hidden translation-era tiles as a ROM Easter egg; they are not inserted into normal gameplay.

## Audio

- Fix the unwanted main-theme restart on ordinary Down+A/crouch gestures, while preserving the required transition out of the existing flight modes.
- Music Off suppresses the main background theme, while allowing other native music-channel sequences such as elevator music and alarms. Their completion/stop commands still work; returning to the main theme while disabled stops the previous sequence instead of leaving it looping.
- Preserve Sound FX as a separate option. Sound Test provides a silent initial selection and explicitly triggered native sequences; selecting another entry stops the previous one. The unhelpful silent entry was removed.
- Correct the identified gas effect's channel panning to both channels without changing its instrument level.
- Stop music during manual password entry. On return, restore the main theme if Music is On; preserve the incorrect-code sound. Avoid unnecessary restarts between menus and restore music after SRAM continuation when enabled.
- At the ending, ensure the main theme is playing regardless of the Music option or an earlier alarm; do not restart it if it is already playing. At credits completion or skip, reset Music to On and let the title start its music at the native point.

## World interactions and persistence

- New ordinary games derive the random seed from start timing, instead of always using the same seed. The native algorithm still performs eight swaps in the existing 16-code table: individual door codes can remain unchanged. Each supplied code has distinct digits. The separate airlock code remains 9831; password starts retain their compatible initialization path.
- Correct Eye's map-bound test and preservation of coordinates during destructible-cell processing, including the eastern map area and fuse-box destruction path.
- Add a bounded 11×11 destructible-cell pass to grenades, in addition to their native dynamic-object damage. Ordinary walls are not converted into destructible objects. Blast damage is still not blocked by walls; no line-of-sight physics was added.
- Extend the destroyed fuse box's blackout-restoration delay using a separate multiplier/countdown. This is a twentyfold delay mechanism, not a guarantee of permanent darkness or a fixed number of real-time seconds.
- Add SRAM checkpoints when the elevator ID-card action generates a password. The extended record supplements that password with the existing per-floor histories, terminal-use flags, body damage, resources, inventory/selection and door-code table.
- Resume Saved Game validates the record and restores the extended state after the native password initialization. Manual Enter Password remains a separate path; it does not silently import unrelated SRAM history.
- Correct unsafe/incomplete body-damage reconstruction in the continuation path that could immediately kill the character. Preserve full damage data when an extended checkpoint is available.
- Retain the original history capacity: 16 entries per floor. This is not storage for every dropped item or every destroyed object. Checkpoints are not full emulator save states; they do not preserve all enemies, exact real-time state or arbitrary destroyed geometry.
- ROM grows from 1 MiB to 2 MiB; header size/checksum are updated. SRAM mapping is declared for compatible odd-byte cartridge SRAM. Hardware and flashcart compatibility still require testing on the intended device.

## Companion atlas and documentation

- Offline Russian and English HTML atlas, 16 maps, cell selection and persistent descriptions, toggleable legend highlighting and nonwrapping floor navigation.
- Original map cells, initial enemy locations, separate respawn annotations, code/randomization notes, access groups, Parking ending condition and L4 Bomb-rescue marker.
- Extracted front-facing enemy previews, ordinary-palette world objects and inventory icons, interaction panels and recorded Screen images, illustrative doors/alarm/laser scenes.
- Fixed information/preview panels, balanced paired images, alpha-cropped panel corners, developer/resource credits, PNG maps and CSV/JSON exports.
- Reproducible cumulative ROM builder and IPS output, source hashes, release notes and CPU-level regression tests. The source builder needs both original regional ROMs; applying the ready-made IPS needs only Cyber-Cop.

## Remaining limits and validation scope

Slow scenes, some original geometry/near-wall visibility artifacts, the limited per-floor history and blast-through-wall behavior remain. This is not a rewrite of all mechanics described inconsistently in the manuals. No new psychic interface, Sega Mouse support, Amiga Mission Disk levels, permanent full-world saving or new LOS explosion model is included.

Tests execute relevant 68000 routines, compare memory/images and model selected hardware operations. They do not replace full Kega Fusion gameplay or physical-console validation. Emulator save states embed old code addresses and are not guaranteed compatible between versions; back up SRAM before upgrading.

## v33 follow-up

- Replace the numeric sleep gain display and its glyph cache with periodic updates of the original Energy bar; native wake-up credits the gain only once.
- Give an intact Gas Mask priority over Face Mask regardless of inventory order.
- Block lockpick activation during the actual game alarm state.
- Clear the leftover Use-block flag at elevator arrival; verify buffered Y invokes Computer exactly once.
- Stop the jetpack sequence on battery exhaustion without cancelling other active sequences; give alarms priority and resume the jetpack after an alarm ends. This does not add simultaneous jetpack/main-theme mixing.
