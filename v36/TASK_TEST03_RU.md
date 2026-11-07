# Test03 — запрос 2026-11-07 после test02
Порядок пользователя: ROM и результат в чат → GitHub/wip → Атлас. Main пока не менять. Накопленные checked fixes сохранять отдельными коммитами после ROM; промежуточные локальные checkpoint обязательны. Не терять список при паузе.

ROM:
- [ ] Holo labels на2 native pixels левее, сравнить пользовательский эталон.
- [ ] Scanman верхняя стрелка при нижней нажатой: вернуть полутона цветом рамки.
- [ ] Шлюз: рамка кнопки активации привязана к штатному latched texture до закрытия.
- [ ] Мемориал: новые приблизительные координаты, Amiga guard с различимыми волосами.
- [ ] Новые props: нижняя повторная полоска при отдельных масштабах; обломки и реакция бочки на выстрелы сравнить с Amiga.
- [ ] Equipment: аватар выбранного персонажа; убрать только ложный entry sound, не первый настоящий click.
- [ ] Только card сдвинуть на1 символ влево (готовность откатить).
- [ ] Lamps toggle после wall stripe в options/sleep, default on; sleep настроку вверх.
- [ ] Профиль производительности по test02.gs0, ускорение ламп; тонкие эллипсы на расстоянии.
- [ ] Mission lift скорость как Original; external lift: расстояние от показанного этажа, wrong direction extra wait.
- [ ] Alarm duration x5.
- [ ] Mission финальные титры сравнить и перенести отличия, сохранить mod credits, проверить40-column centering.
- [ ] Autoaim camera выше emergency lamp, если простая безопасная смена приоритета.
- [ ] Mission8652: определить дверь/шлюз, фиксированный код не должен randomize.

Атлас ПОСЛЕ ROM/wip:
- Mission карты/коды/допуск; две кнопки Original/Mission справа от стрелок. Сохранять floor index, zoom и размеры панелей.
- Лампы: контур клетки; screenshot как alarm-floor preview по эталону.
- Враги: оформление из сравнительного Amiga-атласа.
- Камеры красные круги, аварийные лампы оранжевые.
- Pickup: контрастная центральная точка; rare disruptor/masks/lockpick/etc яркокрасная; embryo container зелёная.

Вложения local upload/: holo_labels02_fixed.png; scanmap brighten up button unpressed/pressed.png; in memory of - new placement*.png; lantern example for atlas.png; Cyber-Cop_v36_test02.gs0. Ресурсы не публиковать в GitHub.
