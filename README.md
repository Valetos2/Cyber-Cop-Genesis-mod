# Cyber-Cop / Corporation — Genesis Improvement Project

**English** · [Русский README](README_RU.md)

**Milestones:** [`main`: v36](RELEASE_NOTES_v36_RU.md) (second Amiga Mission Disk campaign, separate saves, new enemies and lighting); [`wip`: v36a hotfix](https://github.com/Valetos2/Cyber-Cop-Genesis-mod/blob/wip/v36/RELEASE_V36A_RU.md) (indicator palettes, card lenses and elevator arrival display). The game changes in v36a **have not been merged into `main`**. The latest standalone IPS actually stored in this repository is the [v35c patch](patches/Cyber-Cop_v35c.ips); the v36/v36a game ROMs and their private release packages are not hosted here.

**Highlights:** second 16-floor campaign (32 maps total), native Sega Mouse with MouseLook, streamlined controller and inventory input, optimizations and lighting, SRAM checkpoints, new robot and objects, and a companion bilingual Atlas 40. This is an unofficial improvement project, not a remake.

### Making Cyber-Cop the game it always deserved to be.

An unofficial fan-made improvement patch for **Corporation / Cyber-Cop** on the Sega Genesis / Mega Drive.

The goal of this project is simple: **fix what was broken, improve what was frustrating, and preserve what made this unusual game so fascinating in the first place.**

This is not a remake or a graphical remaster. It is an attempt to bring the original game closer to its full potential, with better controls, improved performance, numerous bug fixes, and quality-of-life improvements — without sacrificing its atmosphere, complexity, or identity.

And behind this project is a rather personal story.

---

## What makes Corporation special?

Originally released for home computers in 1990 and later brought to the Sega Genesis / Mega Drive as *Cyber-Cop*, Corporation is a remarkably ambitious first-person action-adventure game.

Years before *System Shock*, it was already experimenting with many of the ideas we now associate with immersive simulations.

You play as an operative infiltrating a heavily secured corporate facility where experiments involving a new life form have gone terribly wrong. Your mission is to reach the laboratories, retrieve a specimen, and escape through the parking area.

Sounds straightforward? It isn't.

The building is a maze of interconnected floors, locked rooms, security systems, surveillance cameras, alarm-triggering floor and laser sensors, hostile robots, and dangerous biological creatures.

Progression requires exploring the building, locating access terminals, obtaining security codes, and gradually unlocking routes to other floors.

But combat and exploration are only part of the experience.

The game also features:

- **Character selection:** Different operatives have different physical attributes and abilities.
- **Equipment management:** Weapons, ammunition, protective gear, and specialized devices.
- **Limited inventory and encumbrance:** Carrying too much equipment affects movement.
- **Fatigue:** Your character needs food, drink, and sleep to remain effective.
- **Individual body-part damage:** Injuries can impair specific abilities or become fatal.
- **Suit energy management:** Electronic devices and certain weapons depend on a limited energy supply.
- **Security systems:** Cameras, alarms, poisonous gas, access restrictions, and electronic locks.
- **Environmental storytelling:** Holographic clues help explain what happened inside the facility.

Exploration requires patience, preparation, and planning. The original manuals even encourage players to draw their own maps, record useful information, and expect to restart the adventure several times before succeeding.

Corporation was an unusually deep and forward-thinking game for its time.

Unfortunately, it was also extremely difficult to enjoy.

## A personal history

### 1996 — First encounter

My fascination with Corporation began in 1996, when I got my first Sega Mega Drive.

I was particularly drawn to first-person games. Driving simulations, flight simulators, and first-person shooters captured my imagination in a way that traditional side-scrolling games rarely could.

I loved the feeling of being *inside* a virtual world rather than simply controlling a character on a screen.

Some of those environments made such a lasting impression that I continued dreaming about being inside them for decades.

There weren't many first-person shooters on the Mega Drive. I was fascinated by the atmosphere of *Zero Tolerance*, the unusual gameplay of *Bloodshot / Battle Frenzy*, and, eventually, the mysterious *Corporation*.

When I bought my copy of Corporation, I had very little idea of what I was getting into.

It was slow, confusing, and complicated. The interface was clumsy, the controls were awkward, and the game explained almost nothing.

But the more I explored it, the more I realized how much thought had gone into its design.

There was something extraordinary hidden beneath all those technical limitations.

I wanted to understand it.

And I never quite managed to let it go.

### 2003 — My first attempt to improve the game

In the early 2000s, I discovered emulators and ROM hacking tools.

Although I had no programming experience, I gradually figured out how the game's graphical tiles, fonts, and text data were organized inside the ROM.

Using a collection of rather primitive utilities — some of them running under DOS — I managed to create a Russian translation of the Sega Mega Drive version.

On **June 27, 2003**, my translation was published by **[SHEDEVR](http://shedevr.org.ru/cgi-bin/gamez.cgi?n=78)**, a Russian console game translation community, under my nickname *Valet2*.

I was incredibly proud of that achievement.

To my surprise, the translation eventually appeared on unofficial physical cartridges. I was even offered a small payment for its commercial use, which I declined. Knowing that I had contributed something to the console gaming world I had grown up loving was reward enough.

About twenty years later, I finally managed to find a physical cartridge containing my translation.

Over the following years, my interest in the game also led me to collect its various official releases: Mega Drive, Genesis, Amiga (including the additional level disk), Atari ST, and DOS on 5.25-inch floppy disks.

I also obtained, scanned, and shared the original manuals, some of which were very difficult to find online at the time.

Reading those manuals revealed something surprising: Corporation was even more sophisticated than I had originally imagined.

And yet, despite all this dedication, **I had never completed the game legitimately.**

### 2026 — The project I thought would never happen

For years, I had a clear picture in my head of what Corporation *could* have been.

Its underlying design was fascinating, but the poor controls, slow rendering, confusing interface, and numerous bugs made playing it an unnecessarily frustrating experience.

I even tried asking experienced ROM hackers whether they would be willing to fix some of these problems for money.

Nothing came of it.

Then, in October 2026, I decided to try something different.

I gave the original ROM to **OpenAI's GPT-6 Astra** and asked it to make the player's turning speed faster.

It worked.

Encouraged by this first success, I asked for something I had previously considered almost impossible: add a subtle horizontal reference line and a shading pattern to the otherwise featureless walls, so that players could better perceive their orientation and movement.

That worked too.

And that was the beginning of this project.

Over the following days, I spent countless hours testing new builds, identifying problems, proposing improvements, and sending feedback to the AI.

One fix led to another. Then another. And another.

What had started as a small adjustment to the turning speed quickly became a substantial effort to repair and modernize the entire gameplay experience.

For the first time in nearly thirty years, the Corporation I had always imagined began to take shape.

---

## Complete changes compared with the original Genesis game

This is a **cumulative feature list through the v36a milestone**, checked against **66 archived README and technical-note files** from v01 onward. Bracketed tags identify the earliest documented build(s) and meaningful later refinements. **MouseLab was a separate test-ROM line**; `integrated v35` distinguishes experiments from released game features. `[v36a]` features are on **`wip` only**; the main-game source release in `main` remains v36. Atlas revision numbers refer to a separate tool. For a detailed chronology and superseded experiments, see [version history](docs/ROM_VERSION_HISTORY_EN.md).

### Controls, movement and Sega Mouse

- Faster turning, with a precise original-sized first step when turning in place; holding the direction accelerates subsequent steps. [v01; fine first step v24]
- The original v02 automobile-style reverse-turn inversion was reverted, keeping conventional backward-turn directions. [v03]
- A+Left/Right adds basic side-stepping without rotating the view. [v03]
- Strafing is blocked during ordinary jumps while horizontal momentum is preserved. [v04]
- Diagonal A+direction strafing uses one shared movement speed; a follow-up fix prevents unintended camera rotation. [v26; corrected v27]
- Jump and crouch gestures are recognized on releasing A; a strafe gesture cannot accidentally trigger them. [v26]
- Context-sensitive A picks up objects and interacts with the world, without breaking movement combinations. [v07]
- A six-button pad is detected while three-button input remains supported; Mode toggles native sleep and waking. [v02]
- Six-button controller detection and Mode-controlled native sleep were added before the XYZ shortcuts. [v02]
- In-game menu navigation now moves only on fresh directional presses instead of unintentionally repeating held input. [v02]
- Short B/C/Start and six-button action presses are remembered during VBlank and consumed once by the game loop; continuous movement is not queued. [v26]
- A missing previously connected controller triggers native sleep at a safe point, where the controller reports a detectable disconnection. [v28]
- Native Sega Mouse support in controller port 2, with captured MouseLook and a free pointer, switched by the middle mouse button. [MouseLab Test01–02; integrated v35]
- Mouse aiming and world/panel/inventory interaction, including single-trigger clicks, visual held-button feedback, and prevention of unintended repeat actions. [MouseLab Test02–09; integrated v35]
- Holding a mouse button over a clickable control displays its pressed state without repeatedly activating the control; drag-in gestures are ignored. [MouseLab Test03–04; integrated v35]
- Adjustable mouse sensitivity and vertical screen-space look offset (not geometric 3D pitch); controller controls remain available. [MouseLab Test02–03; integrated v35]
- Mouse input is suppressed during an accepted elevator journey; frontend Options/sleep-menu controls and the sensitivity slider receive dedicated handling. [MouseLab Test04–09; integrated v35; lift input lock v35c]
- The v35a startup black screen was traced to a conflict between mouse polling during VBlank and the Z80 audio bus and corrected. [v35a]
- Mouse sensitivity-slider VRAM tile corruption and false jump/crouch gestures with a free cursor were fixed. [v35c]
- Mouse-driven character and equipment selection, precise hit areas, a character portrait on the equipment screen, and fourth-button confirmation. [v36 test01–03; released v36]

### Inventory, object panels and interaction fixes

- After using one of several identical consumables, the same item type remains selected; selection advances sensibly when the last copy is gone. [v26]
- Hotkey use now enters the correct native object interface state, including the timed-bomb panel. [v24]
- A quick pickup of a broken item makes Repair the focused inventory action on the next opening if that item remains selected. [v15]
- After inserting an ID card, an available Flying Lead is preselected once; lockpick auto-selection focuses Use. [v26; lockpick v32]
- Automatic ID-card selection at the elevator/terminal now focuses Use rather than leaving the cursor on a backpack arrow. [v18]
- When Use becomes unavailable, the cursor seeks an enabled icon to the left instead of wrapping around to Sleep. [v21]
- When Drop becomes unavailable, it too searches left; manual cursor navigation remains unchanged. [v34]
- Scanman automatically selects an available Screen in the game's priority order and focuses Use. [v34]
- Exterior elevator call buttons no longer forcibly move the cursor or replace the selected item. [v34]
- A stale Use-block flag is cleared when the elevator arrives, so the next Y/use action is not swallowed. [v33]
- Refill and Chemicals cannot be wasted outside their intended refill contexts; world-item preview and dropped-Embryo rendering defects are fixed. [v26]
- A temporary, centered HUD label identifies the selected item without obscuring the underlying interface. [v26; refinements v27–32]
- Bomb confirmation has distinct yellow feedback, while the armed bomb retains its red indicator. [MouseLab Test05–09; integrated v35–v35c]
- A timed bomb's Enter confirms the current value, and changes to the digits clear confirmation; closing an unarmed bomb does not activate it. [v26]
- Opening another object panel now closes the previous one cleanly, avoiding overlapping panel resources. [MouseLab Test09; integrated v35]
- Airlock Enter can move directly right to the yellow action button, and panel transitions use bounded cursor searches. [v24]
- Bomb confirmation feedback, Scanman brightness controls and panel click zones are refined for mouse use. [MouseLab Test05–09; integrated v35–v35c]
- Screen items are labeled Holo. a / Holo. b / Holo. c; Scanman brightness and screen selection reset correctly when re-entering. [v36 test02–04; released v36]
- Closing a terminal restores the affected inventory HUD rows, and Mission's distinct Scanman Screen images are supported. [v36 test02; released v36]
- The original item-breakage flag survives dropping, picking up and floor persistence; an already broken item cannot become repaired by being picked up again. [v36]
- Lock/elevator number palettes are restored, so the green digits remain correct alongside newly shaded red indicators. [v36a]
- Inserted-ID-card indicators on the elevator and airlock receive shading without replacing the original number colors. [v36a]

### Rendering and performance

- Five selectable screen-space wall dithering modes (Off, 2×2, 4×4, 4×8 and vertical bars) replace a single mandatory pattern. [v19]
- The earliest experimental wall shading used vertical screen-space stripes rather than textured 3D walls. [v04]
- The 4×4 Bayer variant was tested before 2×2 was chosen for the main release; the full five-option selector arrived later. [v07; 2×2 v12; selector v19]
- A perspective-projected reference stripe was added to wall faces; subsequent fixes improved its distance shading and near-plane behavior. [v05; v06; v17/v21]
- The horizontal stripe gained correct depth-relative tone and a lower position, rather than remaining uniformly bright. [v06]

- Scene depth sorting was first accelerated without changing the final order of equal-depth items. [v08]
- Projection of ordinary wall centers uses a simpler depth calculation with fewer divisions and multiplications. [v10]
- Continuous ordinary wall segments can hide fully occluded ordinary cells before projection and sorting. [v11]
- Entirely offscreen projected wall surfaces and their reference stripes are skipped before rasterization. [v12]
- Optimized large sprites and destruction animations retain nearest-neighbor sampling and transparency. [v13]
- The 2 MiB ROM expansion houses precomputed pixel-pair data for the largest 64×98 source sprite frames. [v13]
- Ceiling lights and floor pools of light are restored; lamps can be toggled in Options and the sleep menu. [v36]
- Lights are inserted into verified empty cells of the original campaign; optimized ellipse drawing reduces artifacts and some expensive rendering paths. [v36]
- Mission floor/ceiling color bands and imported-sprite trailing strips are corrected; both barrel sprites are lowered consistently in world space. [v36]

### Menus, presentation, sleep and audio

- The main menu now separates Start New Game, Resume Saved Game and Enter Password, with a dedicated Options entry. [v18]
- Cheats became a separate menu/page before the main-menu entry was hidden behind four distinct Down presses on Options. [v31; hidden v32]
- Configurable Music/Sound FX, wall effects, a Sound Test and additional sleep-menu settings; cheat entries include infinite energy/battery, invincibility, access level and Auto Sleep. [v14; sleep settings v16; Auto Sleep v24; cheat pages v31]
- The original game's sound sequences and sound effects can be explicitly auditioned via Sound Test without automatically playing a selection. [v14]
- Sleep acquired an in-game settings page, later expanded to a second page with five cheats. [v16; extended v31]
- Auto Sleep enters native sleep near exhaustion; it is off by default and does not cure existing injuries. [v24]

- A/B/C/Start can skip the scrolling background story; Start can skip earlier logo sequences. [v06; extended v15]
- The two regional title logos alternate without replacing the underlying game with a different regional version. [v14]
- The mod's version number appears on the main menu; the fan credits appear after the original credits. [v23; mod credits v26–28]
- Previously restored tiles from the author's 2003 Russian translation are preserved as an unused ROM Easter egg. [v26]
- The main menu stops at its ends even after Cheats unlock, and its idle timeout is doubled. [v34]
- The world view flashes a separate low-energy warning, initially at 10% and later at 15%, without replacing native empty-battery blinking. [v24; threshold v32]
- The empty-battery flicker follows the original game's sequence and remains separate from the low-energy warning. [v25]
- The sleep Energy preview now uses only the native HUD renderer, preventing the old value from overwriting the recovered value. [v34]
- The separate numeric sleep-energy overlay was removed in favor of the original bar; Gas Mask now takes priority over Face Mask. [v33]
- Sound Test plays native music and effects on explicit command rather than on selecting a row. [v14]
- Music Off mutes the main background theme but permits lift and alarm sequences, and stops a preceding sequence correctly when returning to the main theme. [v23]
- Password-menu entry/return now follows the intended music stop/restart rules, without unnecessary menu-loop restarts. [v20; corrected v21]
- An ordinary Down+A crouch no longer restarts the main theme unless a real flight-state transition requires it. [v13]
- The gas sound's original one-sided panning is corrected to both stereo channels. [v26]
- The ending reliably plays the main theme, while credits completion restores Music On for the next title screen. [v29; credits reset v30]
- Jet Pack audio stops on battery exhaustion but does not silence a higher-priority alarm; the pack sequence can resume after the alarm. [v33]
- An in-memory-of-Kevin-Bulmer screen precedes the Sega logo, using the adapted Amiga portrait; repeat-entry palette/scroll glitches are fixed. [v36 test02–04; released v36]
- Additional shading and held-button feedback are provided for keypad, airlock and bomb indicator lenses. [MouseLab Test06–09; integrated v35c; refined v36]
- The keypad's red alarm lamp now remains lit while the alarm actually blocks access, rather than only flashing briefly. [v32]

### Gameplay, combat, equipment and elevators

- New games vary the native shuffled door-code table instead of always starting from the same random seed; fixed airlock codes remain fixed. [v26]
- The randomized door-code table is preserved in extended SRAM on Resume; the fixed airlock combination is not randomized. [v26]
- Fixed map-boundary and destructible-cell handling for Eye; grenades affect destructible map objects within a bounded 11×11 area (still without wall occlusion). [v26]
- Destroyed fuse boxes keep the lights off longer through an extended restoration countdown, without making blackout permanent. [v26]
- Lockpicks cannot activate while the actual in-game alarm flag is set. [v33]
- Using an already active Jet Pack switches it off and allows the original descent physics to restore standing posture. [v34]
- Alarm duration is increased fivefold; enemy auto-aim prioritizes active threats over cameras and alarm lamps, with additional obstruction checks. [v36 test03–04; released v36]
- Free-cursor mouse aim remains independent of the automatic target-priority rules. [v36 test04; released v36]
- Character equipment creation avoids excess copies of reusable devices and unsuitable medical/mask supplies for the droid. [v36 test04; released v36]
- Elevators retain the original 80-VBlank-per-floor timing across both campaigns; infinite-travel regressions are fixed. [v36 test03–04; released v36]
- Accepted elevator destinations are written into the proper campaign's SRAM checkpoint while Parking/Warehouse transitions remain separate. [v36 test04; released v36]
- A wrong-direction exterior call sends the lift to the opposite extreme floor before returning; further clicks do not reroute an active call. [v36 test05; released v36]
- A wrong-direction lift call includes an additional full floor-time pause at the opposite extreme floor before returning. [v36 final]
- The elevator call panel now shows the final destination floor for a full rendered frame before closing. [v36a]

### Saving, campaigns and new content

- Extended SRAM checkpoints capture character state, inventory, injuries, access and original floor histories when an elevator ID-card action creates a password. [v21]
- Resume Saved Game validates and restores extended data; unsafe body-part damage reconstruction after continuation is corrected. [v21]
- A password-only SRAM save first appeared before the extended history format; the later checkpoint does not become a full emulator save state. [v17; expanded v21]
- The original per-floor history capacity remains limited, so SRAM is not a full emulator save state. [v21]
- Original v35c builds extend the ROM to 2 MiB and retain the required SRAM layout. [v13; SRAM started v17]
- The Amiga Mission Disk is adapted as a second, selectable 16-map Genesis campaign while preserving the original 16-map game. [v36 test01; released v36]
- Each campaign has independent SRAM checkpoints and continuation; passwords select the proper campaign and Continue only appears for valid saves. [v36 test01–02; released v36]
- Mission adds its original map layouts, equipment placement, enemies, respawn data, access progression, prison and scripted alarm behavior. [v36 test01–04; released v36]
- Mission adds a walking/attacking/dying bipedal robot with two PCM sound effects, plus barrel, chairs and chair debris; source enemy behavior is adapted for Genesis. [v36 test01–04; released v36]
- Two additional robotic PCM effects are available in Sound Test as 24 (step) and 25 (attack); only one PCM stream can play at a time. [v36 test01; released v36]
- Mission Scanman imagery and its alternate ending image/text are incorporated; original Genesis credits and mod credits remain available. [v36 test01–03; released v36]
- Mission airlock code 8652, original airlock code 9831, and laboratory code 0451 follow their campaign rules; repeated terminals on the same floor cannot grant duplicate access. [v36 test03–04; released v36]
- Both hidden test maps are isolated from the campaign SRAM slots, so experiments do not overwrite main-game progress. [v36 test02; released v36]
- The first separate test map was available with Sega Mouse integration; a second one was added for Mission actors and scenery. [v35; second map v36 test02]
- The combined game ROM grows to 4 MiB to hold the second campaign and its additional assets. [v36]

### Companion atlas (separate from the game ROM)

- Standalone bilingual offline atlas with selectable map cells, item/enemy previews, access notes, panels and exports. [≤Atlas r37]
- Atlas 40 covers both 16-map campaigns (32 maps), preserving floor/view parameters when switching campaign and language. [Atlas r40]
- Expanded marker legend, resource previews and distinctive airlock-terminal blinking; full exported image packs remain separate from the source repository. [Atlas r40]


---

## Version-by-version history and MouseLab

The [archival release history](docs/ROM_VERSION_HISTORY_EN.md) traces v01–v36a, including the nine experimental MouseLab builds and all five v36 test builds. It distinguishes first prototypes, later corrections and the consolidated main-game versions. The separate [Russian chronology](docs/ROM_VERSION_HISTORY_RU.md) is also available.

## Future plans

The original manuals and other platform versions describe features and gameplay possibilities that are missing, incomplete, or substantially different in the Genesis release.

I would like to investigate whether some of these can be restored or implemented.

Possible future work includes:

- Further performance and rendering improvements.
- Additional fixes for gameplay mechanics and interface behavior.
- Investigation of missing features documented in the original manuals.
- Restoring selected functionality from the Atari ST, Amiga, or DOS versions where technically feasible.
- Further polishing the **already integrated Amiga Mission Disk** campaign through playtesting and targeted fixes.
- Expanding the accompanying ROM analysis and level-viewing tools.

These are ambitions, not promises. The project will develop according to what is technically possible, what can be tested reliably, and how much time and enthusiasm I can devote to it.

Most importantly, I want the game to remain recognizably **Corporation**.

## Downloads, patch compatibility and build status

**The repository does not distribute original or modified commercial game ROMs.**

- **Ready-to-use public patch:** [Cyber-Cop v35c IPS](patches/Cyber-Cop_v35c.ips), for the exact unmodified 1 MiB **Cyber-Cop (W) [c][!]** image (no copier header). See [v35c release notes](RELEASE_NOTES_v35c.md).
- **Latest game sources in `main`:** v36, with Amiga Mission Disk and a 4 MiB output. See [v36 release notes](RELEASE_NOTES_v36_RU.md), [source tree](v36/) and [development state](DEVELOPMENT_STATE.md).
- **Latest milestone in `wip`:** v36a hotfix. Read its [Russian notes](https://github.com/Valetos2/Cyber-Cop-Genesis-mod/blob/wip/v36/RELEASE_V36A_RU.md). A ready-made public v36a IPS is **not** in `patches/`; having sources here does not imply every private input needed for a full rebuild is included.

Original Cyber-Cop SHA-256:

```text
98838ed8d69349ab64a99e4a4e0ea72843d47b175b69fda36957283932f0aba9
```

The **Corporation** regional ROM is also required by the source-based builder for title artwork (but **not** to apply a ready IPS); its SHA-256 is:

```text
226368b1693af2db21bb1cc640b94d5b021c9ff20fcb86207d2b76590503cc98
```

**Never chain cumulative IPS patches at random.** Apply the patch designed for your exact base ROM, or use a specifically labeled incremental patch for its stated earlier build. Keep backups of the original ROM and SRAM. Emulator save states from older versions may point at outdated machine-code addresses. For historical v35c build instructions, see [DEVELOPMENT.md](DEVELOPMENT.md).

## Companion atlas

The separately produced **Atlas 40** covers **32 maps across two campaigns** with Russian and English interfaces, clickable cells, enemies and objects, access and code notes, distinct item markers, equipment/panel previews, and remembered map/view settings. The generated HTML and extracted graphical packs are separate artifacts, not content embedded in the ROM and not necessarily present in this source repository. See [Atlas 40 documentation](atlas39/README_RU.md) and [its source folder](atlas39/). Original game imagery remains owned by the respective rights holders.

## Development tools

The repository also contains or is intended to contain tools used during development, including:

- Python scripts for ROM analysis and modification.
- JSON data files describing game structures and resources.
- An HTML-based level viewer and related inspection utilities.
- Supporting documentation for understanding and modifying the game.

These tools may be useful to anyone interested in researching the internal workings of Corporation or developing their own improvements.

## How was this made?

An unusual aspect of this project is that **I am not a programmer**.

I don't write assembly code or Python from scratch. My background is in exploring the game's behavior, understanding its mechanics, examining ROM graphics, finding problems, and imagining how things could work better.

The technical implementation is developed with the assistance of **OpenAI GPT-6 Astra**.

My role involves defining the changes, explaining the intended behavior, testing builds, identifying regressions, evaluating results, and guiding subsequent iterations.

The AI assists with reverse engineering, code analysis, implementation, debugging, and optimization.

I believe in being transparent about this process.

This project demonstrates how modern AI-assisted development can make certain kinds of preservation and improvement work accessible to enthusiasts who have ideas and technical curiosity, but lack traditional programming skills.

It is also a reminder that generated code still needs careful testing. The AI can make mistakes, and every improvement must earn its place through actual gameplay.

## Credits

**Project creator, direction, testing and coordination:**

Valentin "Valet2" Kozin  
GitHub: [Valetos2](https://github.com/Valetos2)

**AI-assisted technical development:**

OpenAI GPT-6 Astra

For a full list of project contributors, see [CREDITS.md](CREDITS.md).

For historical information about the original game's developers, designers, and publishers, see [ORIGINAL_GAME_CREDITS.md](ORIGINAL_GAME_CREDITS.md).

Contributions and suggestions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

## License and legal notice

Original project code, tools, and documentation for which the contributors hold the necessary rights are provided under the [Apache License 2.0](LICENSE).

Corporation / Cyber-Cop is a commercial game, and its original code, graphics, audio, and other assets remain subject to the rights of their respective owners.

This is an unofficial, independent fan project, not affiliated with or endorsed by the original developers, publishers, or their successors.

The license for this project's original material does not grant rights to third-party game content.

---

## One last thing

After almost thirty years, I may finally be able to play Corporation the way I always wanted to.

To explore its corridors, uncover its secrets, appreciate its atmosphere, and experience the game beneath all those frustrating technical limitations.

Perhaps I'll even finish it this time.

And perhaps, after all these years, I'll finally stop thinking about it.

*Although, considering my plans for the missing features and extra levels... probably not.*

— **Valentin "Valet2" Kozin**, 2026




