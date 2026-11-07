# test03: исследование и проверки

CONFIRMED (2026-11-07): `v36/test_cosmetics03.py` проходит на текущей WIP-сборке. Это локальные CPU/asset-тесты, не полный игровой тест.

- Holo: исходные карты иконок3F520 делили tiles495/496/497. Теперь12 частных tiles, relocation item bank39A9E; три pointer operands4E66/4EA0/FB30. Pixel comparison с пользовательским референсом допускает только1 уровень округления RGB.
- Amiga Mission destruction13F32: индексы28/29/30 ->FF/5D/5E. FF означает неразрушаемость новой бочки. Genesis113E4 изначально имеет0 для этих индексов. HookAB78 выбирает campaign-specific table. Collision height13FC8 versus Genesis11478: new props0..168,0..76,0..76. HookAB14.
- Scanman scan_contrast35: пять полутонов (167,39),(167,40),(166,43),(166,44),(165,47) используют palette2; сильные штрихи3, inset0.
- Airlock callback77A8, native activation785A writesC0 to panel base227E+74=22F2. Border follows this state while mouse on, independent of hold. Swap bounds161,65..175,79. Test double-swap restores all framebuffer bytes.
- Equipment FC66 automatically searches available entries by FC70 callFD16. FD16 includesSFX; FD2A advances silently. Only call displacement atFC72 changed. ManualFD16 retained. Test automatic noSFX, first manual exactly1.
- Portrait: tablesF84C graphics/F864 maps/F7D4 palettes, selected char2A38. Extract16 native tiles, VRAMBE00, palette2 at286C, name rectangleE804. HookFB88 beforefade. All6 CPU paths checked, visual review pending.
- card: native trim removes trailing spaces. Hook name26_draw AFTERtrim adds padding only exact4-byte card. Native packed string table untouched. bomb/mask/cardx centering unchanged.
- Alarm initial countdown immediate7D48:100->500. No repeated retrigger.

HYPOTHESIS: static sprite bottom stripe from read at height into next column. graphics.py/actors.py now use height+2 stride with zero padding; native render scale sweep still required. Robot unchanged (already padded).

OPEN: lamps and lift remaining. Native lamp queue533C,end5338,10-byte entries; builderCFC8,draw45B8,ellipseD4A0. Current test02 clock uses2798 VBlank elapsed16, timestamp0832; compare original versus Mission before changing. External call8C36 sets2186=10 at8C4C; displayed floor260A, actual2182; callback8B08. Alarmclear7CFE,decrement34A0. Airlock code hook airlock_code35 currently lab0451/otherwise native; investigate Mission8652. Credits v34 build around credits26, nativeBB6. Do not re-disassemble entire ROM.
