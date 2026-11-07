# DEVELOPMENT_STATE

Обновлено: 2026-11-07. Рабочая ветка: **wip**. `main` не изменять без отдельного указания Valentin / Valet2.

## Текущая задача
Выполнить пользовательский список v36 test03: сначала ROM, затем публикация результата в wip, затем Atlas Mission. Полный список — v36/TASK_TEST03_RU.md. Текущий промежуточный checkpoint НЕ является готовым релизом. Main не изменена.

## База и последний рабочий результат
- Публичная база main: `d19384256a2761625e6b3c91d7fc916fbe35f059` (v35c + Atlas r37 source update). Это рабочая опубликованная база; main оставлена без изменений.
- Кандидат для игрового теста: **v36 test02**, передан 2026-11-07. Его точный hash и hashes приватных входов — `docs/input_manifest.json`.
- Последний проверенный исходный checkpoint v36: `7329c216a7afaeb8b8992c6fce05d527d1f1c0b0` — `checkpoint: preserve validated v36 test02 sources; gameplay approval pending`. Он отправлен в GitHub/wip. Это checkpoint выполненных проверок, а не одобрение пользователем игрового релиза.
- Правила и база знаний: `561e81fffac52878b27885cabe8bffbb63628579`. Последующий docs-коммит только записывает SHA checkpoint; не является новой игровой сборкой.

## Что изменено в test02
Лифт: elapsed VBlank вместо совпадения фазы; lab01: сохранён вход4966; лампы: подключён rasterizer; палитры: цветные полосы Mission; HUD: восстановление строк после закрытия терминала; frontend: зоны клика/скрытие arrow/ПКМ без действия; Holo labels; Scanman Mission; lab02; мемориал; компактные Continue.

Подробности и доказательства: `docs/reverse-engineering/BUGS.md`, `ARCHITECTURE.md`, `BUILD_AND_TEST.md`, `addresses.csv`.

## Уже выполненные проверки
2026-11-07, до задачи организации Git: все девять CPU suites из BUILD_AND_TEST — PASS; BlastEm frontend, lab02 Start, Reset, memorial skip/автоокончание — PASS. Проверены 32 карты,196 пар lift destinations, SRAM/пароли двух кампаний, шесть шлюзовых переходов, robot attack/death, PCM параметры. Чистая пересборка из архива совпала побайтово. Полное прохождение/реальное железо/физическая мышь не проверены.

## Проверки процесса сохранения
2026-11-07: синтаксический AST-разбор всех публикуемых Python-файлов; 4 теста фильтра; интеграционные проверки staged-content, запрета main и запрета бинарного файла — PASS. Проверено 71 предлагаемое текстовое содержимое. Игровые проверки повторно не запускались: исходники test02 в этой операции не менялись.

## Открыто и что дальше
1. Пользователь протестировал test02 и предоставил список правок; сейчас выполняется test03.
2. HUD-01: сохранение исправляется восстановлением панели, но первопричина записи0220 в EA3C не установлена. Повторить терминал/зарядку при новом воспроизведении.
3. При новой ошибке сначала искать в документации и исходниках; локально исследовать только относящийся диапазон.
4. Атлас Mission отложен по желанию пользователя. На этой стадии Atlas r37 не менять.
5. Дальнейшие изменения — отдельные проверенные коммиты в wip; длительные незаконченные шаги — WIP (unverified). Merge/main — только по отдельному указанию.

## Восстановление после паузы
Прочитать этот файл → docs/reverse-engineering/README.md → нужный тематический раздел → проверить фактический удалённый HEAD wip и локальный diff. Приватный комплект test02 хранится отдельно у пользователя; не публиковать его ZIP/ROM/savestate. Публичный checkpoint содержит код и метаданные, а не игровые ресурсы.

## Продолжение test03 — промежуточный checkpoint
Проверено CPU-тестом `v36/test_cosmetics03.py`: Holo pixel reference; Mission stools ->5D/5E debris and intentionally indestructible barrel; projectile height tables; five Scanman intermediate pixels; airlock latched frame/restoration; silent automatic equipment skip and audible first manual action; card-only centering; alarm counter500; six selected equipment portraits.
Изменения сборки: build.py подключает cosmetics03.py; screens02.py переносит item bank с частными Holo tiles; graphics.py/actors.py добавляют два прозрачных ряда под статическими спрайтами; memorial02.py использует Amiga guard и новое расположение.
НЕ ПРОВЕРЕНО окончательно: padding как причина нижней полосы; визуальная проверка портретов/мемориала в BlastEm; полная регрессия. Тестовая сборка собирается, но пользователю ещё не выдана.
ОСТАЛОСЬ: светильники (опции/сон/производительность/масштабирование), лифт (скорость/вызов), автоприцел, Mission8652, финальные титры, визуальная и игровая проверка; затем Atlas. Исследованные адреса и готовые проверки — docs/reverse-engineering/TEST03.md. Не начинать анализ заново.
Последний удалённый HEAD перед этим checkpoint: f819d69b96e8cec40f0c7bfc21bf5d1301760f4e. Точный SHA нового checkpoint проверяется после отправки.

## Проверенный результат test03
2026-11-07: test03 ZIP передан пользователю. Все14CPU suites прошли; IPS roundtrip/checksum PASS. BlastEm подтвердил native lift80VBlank и test02 erroneous20VBlank; новыйthreshold80. Визуально проверены мемориал Amiga, equipmentportrait, optionslamps, sleep. Исходники сохраняются в отдельных тематических коммитах wip. Main не изменена.
Предыдущий WIP checkpoint:33e1f7cf0f039242cf91e8333000c1cb5195de44. Он не включает второй этап lights/lift/aim; после тематических коммитов читать текущийHEAD. Подробности TEST03.md. Отметки OPEN выше исторические: ROM-список выполнен, ограничения проверки сохраняются.
Текущая следующая задача: Atlas38 — Mission campaign, markers/previews/codes/access and state-preserving buttons. Источник atlas37/template.html/build scripts, данныеAmiga maps.json иv36. Не начинатьROMисследование заново. Пользовательское прохождение test03 ещё не выполнено.
