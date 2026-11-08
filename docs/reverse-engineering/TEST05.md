# test05 — barrel placement, elevator calls and indicator shading

CONFIRMED 2026-11-08; user gameplay approval pending. Base main/wip529f103419f89f26b68232fb4034b05628683a02.

Barrels: native B8B0 immediate0054→0040; actors.py newbarrel centre h*2-20. Both lower sprite centre20worldunits without changing bitmap, collision radius64/84 or projectile height tables. Six-cell native renderer comparison matches supplied edit Y316..435 at4x. This is a requested visual adjustment, not proof of an original developer error.

External lift: RAM085E waypoint added;0858timestamp/085Atotal/085Cstep retained. Wrong up goes to display0 then target; wrong down goes26 then target. Codes increment2 per floor,80VBlank each. Equal-floor waits80. Tick handles multiple elapsed steps; native internal elevator unchanged. Busy guard8C36 (12bytes, replay up store explicitly) prevents native latch changes before8C4C. 38C8 wrapper uses existing mouse ownership/hover; overlays C1/C2 only while held and restores7E30long after native rendering. First call remains latched. Both idle directions and busy action guard tested.

Indicators: separate32KiB tile banks for keypad/airlock (assets within existing4MiB ROM), onlyB2lens pixels modified. Keypad palette18052 entriesA/B become red; greenC/D/E unchanged. Airlock uses existing8/A/1reds. Bomb existing bank196000 E1 takes nativeB1lens shape; palette1813A entryA dark yellow,1yellow,7white. EntryB retained after preview revealed that it is also used by bomb display. Comparison tests restrict changes to lens regions:20/20/8pixels. ArmedB1bomb bytes unchanged.

Version text is drawn by main36_text atE800+2*(40-len(label)); prior build only modified the unused old menu string. CPU text-hook verifies v36 test05. BlastEm reaches menu and screenshot.

16 CPU suites passed; see REPORT_TEST05_RU.md. Main remains unchanged pending user approval. Other open test04 investigations are unchanged.
