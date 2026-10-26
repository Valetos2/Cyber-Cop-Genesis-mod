from pathlib import Path
import re
pairs='''Атлас подготовлен GPT-6 Astra по запросу Valentin «Valet2» Kozin · 2026|Atlas prepared by GPT-6 Astra at the request of Valentin “Valet2” Kozin · 2026
Коды обычных замков: исходные значения оригинала / v25. В новой игре v26+ они перемешиваются. Шлюз: всегда 9831.|Keypad codes: original / v25 values. New games in v26+ shuffle them. Airlock: always 9831.
Щелчок закрепляет клетку. Повторный щелчок по типу в легенде снимает подсветку. Щелчок вне карты и панели снимает выделение.|Click to pin a cell. Click a legend type again to remove its highlight. Click outside the map and panel to clear the selection.
Доступ (каждый следующий включает предыдущие):|Access levels (each includes all preceding levels):
и Warehouse — отдельные переходы.|and Warehouse have separate entrances.
клетка $0E для повторного появления. ● — исходный враг из отдельной таблицы; эти координаты не совпадают с S. Спрайты показывают анфас в обычной палитре выбранного этажа; предметы — свою иконку из рюкзака. Для дверей показан рендер с расстояния шести клеток, для тревожной клетки — трёх клеток; R на L4 — место спасения с Bomb. Луч показан в режиме Visor 1: три соседние клетки в восьми клетках от игрока, камера в прыжке. Рядом с объектами показаны их интерфейсы; у терминала — после вставления карты, у Screen — после загрузки записи. Свет и газ — состояния этажа, а не самостоятельные клетки.|respawn cell $0E. ● is an initial enemy from a separate table; these positions do not coincide with S. Enemy sprites face the viewer and use the selected floor's normal palette. Pickups use their inventory icons. Doors are shown from six cells away; the alarm tile from three. R on L4 marks rescue with a Bomb. The Visor 1 preview shows three adjacent beam cells from eight cells away, with the camera raised for a jump. Interaction panels appear beside objects: the terminal after inserting the card, and Screen images after loading the recording. Lighting and gas are floor states, not separate map cells.
В атласе использованы карты, графика, спрайты и палитры оригинальной игры|This atlas uses maps, graphics, sprites and palettes from the original game
версия для Sega Mega Drive / Genesis (1992). Превью сцен получены её рендерером.|for Sega Mega Drive / Genesis (1992). Scene previews were produced by its renderer.
Имена приведены по финальным титрам версии Genesis. Права на оригинальную игру и её ресурсы принадлежат их соответствующим правообладателям. Исторические титры не устанавливают нынешнего владельца прав. Этот неофициальный атлас не связан с оригинальными издателями и разработчиками.|Names are taken from the Genesis end credits. Rights to the original game and its assets belong to their respective rights holders. Historical credits do not establish current ownership. This unofficial atlas is not affiliated with the original publishers or developers.
Оригинальная игра и её авторы|Original game credits
Дизайн и графика:|Design and graphics:
Музыка и звуковые эффекты:|Music and sound effects:
Программирование:|Programming:
Продюсирование и авторские права в титрах игры:|Production and copyright as credited in the game:
Разработка:|Development:
Руководитель проекта:|Project manager:
Руководство:|Manual:
Тестирование:|Quality assurance:
редактор —|editor —
Группа зависит от света; Disruptor не действует.|Affected by lighting; immune to the Disruptor.
От света не зависит; уязвим к Disruptor.|Unaffected by lighting; vulnerable to the Disruptor.
После обычного смертельного урона восстанавливается.|Recovers after normally lethal damage.
Не перемещается; атакует вблизи.|Stationary; attacks at close range.
Восстанавливающийся робот|Regenerating robot
Двуногий мутант|Bipedal mutant
Двуногий робот|Bipedal robot
Робот на гусеницах|Tracked robot
Неподвижный краб|Stationary crab
Человек|Human
Выберите клетку|Select a cell
Исходный враг|Initial enemy
Точка появления; сценарная клетка $0E.|Respawn point; scripted cell $0E.
Возможные враги:|Possible enemies:
Повторное появление на этом этаже отключено.|Respawning is disabled on this floor.
Открывает соседнюю дверь лифта и обновляет таймер закрытия.|Opens the adjacent lift door and refreshes its closing timer.
Открывает соседнюю дверь по|Opens the adjacent door along
оси Y карты (вверх/вниз).|the map Y axis (up/down).
оси X карты (влево/вправо).|the map X axis (left/right).
с исправным embryo ($1E) в рюкзаке запускает финальный экран и титры. Без него не действует.|starts the ending and credits if an intact embryo ($1E) is in the inventory. Otherwise it has no effect.
перенос сюда с исправной Bomb. Один раз за сессию; восстанавливает энергию, голову и туловище.|teleports here with an intact Bomb. Once per session; restores energy, head and torso.
Спасение с Bomb · X42 Y14|Bomb rescue · X42 Y14
Спасение при смерти|Rescue on death
Выход / концовка|Exit / ending
Игровой рендер с расстояния три клетки|Native render from three cells away
Игровой рендер с расстояния шесть клеток|Native render from six cells away
Луч Visor 1 с расстояния восемь клеток|Visor 1 beam from eight cells away
Начальный интерфейс взаимодействия|Initial interaction panel
Панель рисуется геометрией стены, отдельного спрайта нет.|The panel uses wall geometry; there is no separate sprite.
Противник спереди|Enemy front view
Объект в мире|World object
Предмет в рюкзаке|Inventory item
Нет кодовых панелей|No keypad panels
исходный; случайный в v26+|original; randomized in v26+
оригинал / v25; в v26+ случайный|original / v25; randomized in v26+
фиксированный|fixed
Предыдущий этаж|Previous floor
Следующий этаж|Next floor
Увеличить|Zoom in
Уменьшить|Zoom out
Как читать карту|Reading the map
Легенда этажа|Floor legend
Замки|Locks
Код:|Code:
Байт:|Byte:
мировой Z:|world Z:
атлас 16 уровней|16-floor atlas
уровней|floors
Этаж|Floor
Объект|Object
Пол / пустая клетка|Floor / empty cell
Стена|Wall
Клетка дверного проёма|Doorway cell
Лазерный детектор|Laser detector
Детектор / луч|Detector beam
Голографический проектор|Holographic projector
Зона лифта / перехода|Lift transition zone
Точка появления · сценарная клетка 0E|Respawn point · scripted cell 0E
Растение|Plant
Сигнальная лампа|Alarm lamp
Кресло|Chair
Стол|Desk
Бочка|Barrel
Капсула с объектом|Occupied capsule
Пустая капсула|Empty capsule
Барьер / тревожная зона|Alarm floor tile
Ящик|Crate
Колонна|Column
Триггер / переход 1B|Trigger / transition 1B
Шлюз: код 9831|Airlock: code 9831
Терминал (window)|Terminal (window)
Кодовый замок|Keypad lock
Пульт внутри лифта|Interior lift panel
Вызов лифта|Lift call panel
Камера|Camera
Дверь|Door'''
pairs+='\nШирина панели|Panel width\nВысота превью|Preview height\nНачало новой игры|New game start\nПрибытие из G|Arrival from G\nПрибытие из Warehouse|Arrival from Warehouse\nПрибытие из Parking|Arrival from Parking\nПоявление игрока / ориентир прибытия|Player start / arrival reference\nТочка зависит от положения игрока у пульта; показан пример из центра его клетки.|Position depends on where the player uses the panel; this example uses its cell centre.\nПример маршрута: security access|Example route: security access\nНа новом этаже доступ +1, максимум 7. Значение зависит от порядка посещения.|A new floor adds one access level, capped at 7. The result depends on visit order.\nориентир; координаты зависят от позиции у шлюза.|reference; coordinates depend on position at the airlock.\nПереход →|Travel to →\nориентир X|reference X'
translations=dict(line.split('|',1) for line in pairs.splitlines())
s=Path('atlas35/Cyber-Cop_Atlas.html').read_text()
for ru,en in sorted(translations.items(),key=lambda x:-len(x[0])):s=s.replace(ru,en)
s=s.replace('lang="ru"','lang="en"');left=re.findall('[А-Яа-яЁё]+',s);assert not left,set(left)
Path('atlas35/Cyber-Cop_Atlas_en.html').write_text(s)
