# v36: холодный запуск на Mega Drive (OPEN)

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
