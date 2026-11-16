# v36: холодный запуск на Mega Drive

## K confirmed on the user's Mega Drive

User confirmed an actual boot on the affected console/cart, successful load of the existing save, and start of a new game in each campaign. New save write and persistence after resetting/power cycling were not separately reported. K is the playable compatibility baseline, independent of the remaining sleep-menu work.

Carry forward the known-good combination: Z80 boot source at $1F8000, v35c loader-facing title fields, SRAM header preserved, and deterministic non-FF padding before and after the upper asset block. The header checksum must match the output ROM. Reproduce K byte-for-byte from the normal build before applying gameplay changes. This test does not determine whether the cartridge skips erased areas, has a loader heuristic, or fails for another internal reason. In particular, the title-field dependency and the roles of the initial gap and recalculated checksum were not isolated.

## Первоначальная диагностика

- v35c имеет размер 2 MiB, v36b test01 — 4 MiB; заголовок указывает пределы 0x1FFFFF и 0x3FFFFF соответственно. SRAM header и строка регионов совпадают. Проблема на физической приставке заявлена начиная с v36; точная точка остановки неизвестна.
- В v36 перехват по 0x394 вызывает мемориальную заставку до штатной загрузки SEGA. Заставка читает данные выше 2 MiB, использует общую процедуру передачи графики через RAM/VBlank и дополнительно очищает CRAM прямой записью. Это отличия стартового пути, не доказательство причины.
- build_boot_probe.py восстанавливает ровно две инструкции 0x394..0x39B из пути v35c, задающие параметры штатному вызову 0x39C. Пересчитывается контрольная сумма; весь прочий код и область ROM выше 2 MiB идентичны test01. Скрипт требует точный SHA256 исходной сборки.
- BlastEm: холодный запуск test01 J, probe J и E достигает main36_text (0x1F0438); это не тест на физической приставке.
- На одном устройстве/картридже и с одним регионом сравнить test01 и probe после выключения питания. Если работает только probe, искать в вызове заставки и её данных. Если оба не работают, проверить 2 MiB v35c на той же конфигурации; успех v35c не доказывает, что размер — причина, но делает чтение верхней половины ROM и конфигурацию картриджа важной гипотезой. Если работают оба, уточнить условия первоначального сбоя. Зафиксировать последний экран и звук.
- SHA256 probe: f99150cffcbd9ffda2d288589a66d9cfbe383a92aca66857ba0e2f3de051516a.

## Проверка на железе: обе ветки не стартуют

Пользователь проверил обычный test01 и вариант без заставки на настоящей приставке: оба не загрузились. Отключение мемориального экрана недостаточно. Результат контрольного запуска v35c на том же устройстве и картридже пока неизвестен.

Следующий контроль — исходный v35c (2 MiB) против v35c с заполнением верхних 2 MiB байтами FF (изменено только поле ROM end в заголовке нижней половины, остальное совпадает, включая checksum). Успех обоих показывает, что картридж принимает образ 4 MiB, но не проверяет чтение данных из верхней половины. Неуспех только варианта 4 MiB сужает поиск до смены размера/заголовка и режима загрузки. Если не стартует даже оригинальный v35c, сравнение этого прогона не локализует регрессию v36.

Скрипт: v36/build_boot_size_control.py. SHA256 контроля: 7acea947eb1cfb0a7e610b251a3e22a319b2dc230a0af60b793cbf714981c0af.

## 4 MiB control starts on real hardware

User confirmed that the padded v35c boots on the console. File size alone does not account for the failure. The next probe uses this exact control as its base and checks distinct markers at `$220000`, `$260000`, and `$2AA000` immediately before stock SEGA setup. Match: boot normally. Mismatch: stop without drawing SEGA. The probe does not enable SRAM or test access while SRAM is enabled. A pass tests selected reads at boot, not every address or transfer mode.

The 68000 execution check reached `$39C` with all markers present; separately replacing each marker with erased bytes took the intended failure branch. Hardware result pending. Script: v36/build_boot_upper_probe.py. SHA256: 1ac42854193d0a9407d2311b3e15901649c899e7116c9123b7324ce24cc8e346.

## Upper-read probe does not show SEGA on hardware

User reports the upper-only probe does not start. The padded v35c control worked; the failed probe alone cannot distinguish a data mismatch from trouble executing the new hook.

- A (`lower`): same hook, comparisons and upper markers as earlier; compares copies of the markers at `$1F0100..$1F010B` instead. If A also fails, the upper-read result is not interpretable on its own.
- B (`sram_off`): same upper comparisons as earlier, but writes zero to `$A130F1` just before checking. If B succeeds, explicitly changing that register helps on this configuration; keep it a hypothesis for v36 until verified with v36 itself.
- A succeeds/B fails: the hook is executable, but the checked upper reads are not resolved by disabling the SRAM gate. Identify exact cartridge/configuration before choosing the next probe.
- Both variants passed 68000 emulation checks of the continuation, individual corrupted markers, and expected state of the SRAM register at exit. Hardware results pending.

## Hardware: A passes; B fails

This confirms the lower comparison/control path is executable. Neither upper probe with the SRAM header succeeded; writing zero to $A130F1 was insufficient. This is not evidence that all upper addresses fail. Variant C is byte-identical to B apart from the SRAM declaration at $1B0..$1BB, allowing a test of how the cartridge or loader chooses its mode. Verified distinct header and success/failure CPU paths; pending hardware result and cartridge/loader identification. Stop at SEGA or menu, no need to try saving. SHA256 C: 63ab43ccb0ee2a42def91042f9e6e43d5c9bb2ec80d79cf0940c40cf60e10541.

## Hardware: C fails on Chinese EverDrive-MD clone

Firmware version unknown; user reports other 4 MiB ROMs launch on the same cart. Removing the SRAM declaration did not make the previous read-and-stop test pass. D reports read values in the v35c title menu instead of intentionally stopping. Keeps C's header and gate state, and fills the upper bank with non-erased diagnostic data so this test also exercises a fully occupied upper half. ROM addresses in displayed order: `$200000 $220000 $260000 $2AA000 $3FFFFE`. Expected `rom 915e a55a 6d92 f00d be71`; the original first-half words at the corresponding modulo-2-MiB addresses can be compared if hardware reports other values. A success here would establish that these sampled words are readable with this image, not that the previous failure was definitely related to padding.

CPU execution verified correct data and a wholly erased upper half: both return to the stock boot, with expected distinct RAM strings. Hardware result pending. SHA256 D: f97ee3f4b8db8aa5ef4c408fc54f31c14a51148f447914acf7eadf890a237c03.

## D passes on hardware; tail-only test E

On the real EverDrive-MD clone, D boots and displays exactly `rom 915e a55a 6d92 f00d be71`. The upper address space is demonstrably readable with that image. D differs from B/C in more than padding (notably reports word reads rather than comparing longwords), so the cause of B/C and v36 failures is still open.

E starts from confirmed test01 and changes only the erased tail at and above `$2AA392`. Entire header, checksum, code, resources, early upper gap, and physical file size unchanged. This isolates trailing padding. BlastEm reached the normal menu. Hardware result pending. SHA256 E: fee026d9cce2fabe0360f09c9b0220be8be24d48ba59bee7929ec9ef48637f74.

## E fails on hardware; isolate the early Z80 copy with F

User reports E does not work. Changing the trailing padding alone is insufficient. Before any splash, the startup path through $366 calls $15062, with the driver upload at $1567A–$1568C. The 68000 copies 5120 bytes to Z80 RAM byte-by-byte. v35c reads the driver from $0157A8; v36b reads it from $2408AC, above 2 MiB. D only sampled 16-bit words and did not exercise the audio startup transfer.

F is a private test01-based ROM with the identical modified Z80 image copied to the unused $1F8000 region and only its startup source pointer changed. The original upper copy is kept, preserving existing pointers. Header checksum recalculated; all other bytes identical to test01. 68000 emulation verified the entire native copy into Z80 RAM; BlastEm booted to the title menu. Hardware result pending. SHA256 F: 89873b4b91ff3a66cb8d8ae1cf9d90cf4da93f5b95437fde9f1a13788963dfa7.

## F boots on hardware, with corrupted startup screen and menu text

User reports yellow screen and, on Start, main menu with red squares instead of text. Moving just the startup Z80 image below 2 MiB allowed execution to reach the menu. Text strings for v36b main menu are in upper ROM near $228168, while the memorial graphics and palette are near $25601E and $257EBE. Corruption is consistent with bad reads but can involve mode/timing/transfer width; not established that every upper read fails.

G keeps the actual v36b upper half byte-for-byte, including padding, and uses the v36b header with only the checksum recomputed. Lower half contains the known v35c boot/menu plus a diagnostics hook. At the same point as D, with explicit SRAM gate zero, G takes a word read and two separate byte reads at each of $228168, $2408AC, $257EC0, $25625E. Expect both lines to show 7374 f3ed 002e 0000, labelled w/b. Both capture and display verified in emulation. Hardware result pending; G is not a playable v36 build. SHA256: 28d60b5a5a7e5f732de3115435cea2a58552f3731a225b1fe93d83f151ca79c0.

## G boots on hardware but reports bad upper data

User photograph: `w 76ff 7600 76ff 76ff`, `b e1ff e100 e1ff e1ff`. Neither access width returns the expected words. The invariant high bytes match nearby instruction encodings in G ($76 from MOVEQ, $E1 from LSL), consistent with a bus that is not fully driven by ROM; this is a hypothesis, not an established wiring fault.

H retains G's exact probe code and upper asset block. It uses the working D's header (recomputing checksum) and copies D's nonblank filler into both the gap before the asset block and the trailing region. BlastEm reached the title; 68000 checks verified both expected output lines. If hardware reads are now correct, separate the header from filler before proposing a release fix that preserves SRAM. SHA256 H: 612ecaddce22a9e0028c8309dc5a11de3c3de66b3ba2709b496b1a6986804767.

## H reads real upper assets correctly on hardware

Photo: `w 7374 f3ed 002e 0000`, `b 7374 f3ed 002e 0000`. Real v36b data is accessible on this clone with the H layout. Split diagnostics derived from the same H, with unchanged probe code and asset block:

- I restores only the 12-byte SRAM header declaration, preserving D filler, title, and checksum. SHA256 692b20edc62d7f6c9184f50181d9b97b4fff8de315eb259b14de9f46bb020032.
- J restores only the erased upper padding before and after the assets. H's title and blank SRAM header remain; checksum recomputed. SHA256 356b0f873096d02310c163dee080b2f41242f1fb6fbac17ab9c4f23eacaf2eeb.
- Both reach the stock startup continuation with correct w/b values in CPU emulation. Hardware verification pending. If both pass, the remaining combined effects (or header identity) still need testing. These probes are not actual v36b gameplay builds and do not validate SRAM persistence.

## I passes on hardware; J reproduces the bad reads

I gives the expected codes even with the SRAM declaration. J returns the same incorrect codes previously seen with G when the free regions before and after the asset block are erased. This confirms the effect of the free-region layout plus its derived checksum in the H/I/J diagnostics. It does not isolate the initial gap from the tail or prove how the loader detects the layout. The successful I retained the v35c title fields, so the playable K retains them as well.

K combines F's full game code and low Z80 startup image with I's complete upper half and loader-facing header (checksum recalculated). The SRAM declaration and runtime SRAM code remain intact. BlastEm cold boot reached v36b title code; CPU tests passed all 32 maps, both campaign passwords and SRAM namespaces/full restores, and the menu plus busy lift-call guard. Console artwork, gameplay and persistence remain to be confirmed. SHA256 K: 0f86f8421e65feecf44c8569f69ac8095446d3d01b73011ba1cc78a330ff2053.
