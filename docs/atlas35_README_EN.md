# Cyber-Cop — 16-floor atlas, revision 35

Companion to ROM v33. Atlas revision numbers are independent of ROM versions.
Extract the entire archive and open Cyber-Cop_Atlas.html. The initial language follows the browser language: Russian for ru, English otherwise. En / Ru buttons override it; the choice is remembered when localStorage is available. You can also open Cyber-Cop_Atlas_en.html directly. Both files must remain together for language switching. Images are embedded; no network connection is required.

Click a map cell to pin its information; click outside the map/panels to clear. Click a legend entry to highlight matching cells, and click it again to turn the highlight off. Initial enemies appear first in the legend; S marks respawn cells. The information and image previews remain fixed while the legend scrolls. Floor arrows stop at either end.

This revision removes wall enhancements from door previews, crops interaction panels with transparent outer corners, isolates the recorded Screen 1–3 images from the Scanman body, balances object/panel preview sizes, and adds English UI text and spaced access-level groups. The laser preview uses native projected geometry from eight cells away with a raised camera; the three quads are rasterized separately using bright phases of the original Visor 1 palette. It is a static illustration, not an unmodified gameplay screenshot.

Door codes shown are original reference codes, not codes read from your saved game. New games in v26+ shuffle the existing table with eight swaps, so a particular code can remain unchanged. The airlock retains 9831. Parking requires the embryo; R on L4 marks the Bomb rescue location.

Includes two HTML files, 16 PNG maps, extracted sprites/panels, map data, source scripts and test results. Original text inside game images is unchanged. Historical research notes and PNG map captions remain in Russian. Research scripts still depend on local ROMs, save states and previous builds; the finished HTML files do not.

UI tests use a DOM model; full visual browser testing was not performed. Original developer credits and a game-resource notice appear in the atlas. Original game resources remain subject to their owners' rights.

Atlas prepared by GPT-6 Astra at the direction of Valentin “Valet2” Kozin, 2026.

## Revision 35

Keypad previews show each floor's original code; the airlock shows 9831, using the native digit renderer. Terminal access is an example for the route 5F → 4F → Parking → L2 → L7 → L5 → 3F → L4, not a fixed per-terminal reward. The game increments access once per newly used floor, capped at 7.

Drag the vertical divider to resize the sidebar, or the horizontal grip below the preview to resize its height. Keyboard arrows also work when a grip has focus. Terminals blink at two cycles per second. P marks the initial 5F position and example airlock arrival coordinates; airlocks transform the current player position, so arrivals are not fixed spawns.
