# Cyber-Cop / Corporation — Genesis Improvement Project

**Current development build: v34.** See [cumulative changes](CHANGELOG.md), [release notes](RELEASE_NOTES_v34.md) and [build instructions](DEVELOPMENT.md).

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

## What has been improved?

The following changes have been developed for the Sega Genesis / Mega Drive version.

### Controls and movement

- Faster and more responsive turning.
- Strafing support for more natural first-person movement.
- Improved directional control behavior.
- VBlank-based buffering for discrete action presses, reducing missed inputs during slow frames without turning movement into queued steps.
- Six-button controller support: X/Z cycle backpack items, Y uses the selected item, and Mode toggles sleep.
- Contextual A interaction/pickup and finer initial turning steps while stationary.
- More convenient interactions with objects and the inventory: invalid Use/Drop icons fall back to the left, Scanman focuses Use after selecting a Screen, and exterior lift call buttons preserve the cursor and selected item.

### Graphics and performance

- Reduced slowdowns through rendering optimizations.
- Improved visual orientation in corridors and rooms.
- Selectable screen-space wall dithering and a horizontal wall stripe, with separate options to disable either effect. The dithering is not a perspective-mapped wall texture.
- Rendering and visual improvements intended to preserve the original game's style.

### Gameplay and bug fixes

- Fixed various problems with environmental damage handling.
- Added varied door-lock codes between new games. The original game reinitializes its random generator with a fixed seed, producing repeatable codes. The native eight-swap shuffle can leave individual codes unchanged. The fixed airlock code remains 9831.
- Added low-energy warning flashes at 15% or below, optional Auto Sleep before fatal exhaustion, and a periodically refreshed native Energy bar during sleep, drawn by the native HUD alone to prevent competing old/new readings.
- Give Gas Mask priority over Face Mask; block lockpick activation during alarms; clear the leftover Use block on elevator arrival.
- Toggle Jet Pack off by using it again, returning to standing with native descent physics. Stop the jetpack sequence when its battery runs out without cancelling other active environmental sequences. Alarms take priority; simultaneous jetpack/main-theme mixing is not implemented.
- Corrected numerous issues discovered through gameplay testing.
- Added optional infinite energy, infinite battery, invincibility, and selectable access levels, plus a sound test.

### Interface improvements

- Improved automatic cursor positioning during certain interactions.
- Added identification of the currently selected inventory item.
- Improved contextual controls and interface responsiveness.
- Fixed visual and functional issues in several interface elements.
- Added music, sound-effects and wall-appearance settings to the sleep menu, with cheats on a second page.
- Hide Cheats in the main menu until four separate Down presses on Options; navigation remains bounded at both ends after unlocking it.
- Improved front-end navigation and intro skipping. Main-menu idle timeout is doubled. Both regional title logos alternate between title-screen visits.

### Saving and continuing

- Added SRAM-based checkpoint functionality.
- Checkpoints are written when an ID card produces a password in the elevator. They supplement the original password with selected character and floor-history data.
- Manual password entry remains available. A password is not equivalent to the extended SRAM checkpoint.
- SRAM is not a full emulator save state: exact moment-to-moment world state, every dropped item, and permanently destroyed geometry are not preserved. The original per-floor item-history limit still applies.

The objective is not to eliminate the game's difficulty, but to eliminate unnecessary frustration caused by its technical shortcomings.

**Note:** Some improvements may evolve or change as development continues. Detailed technical changes and version-specific features will be documented in release notes.

---

## Future plans

The original manuals and other platform versions describe features and gameplay possibilities that are missing, incomplete, or substantially different in the Genesis release.

I would like to investigate whether some of these can be restored or implemented.

Possible future work includes:

- Further performance and rendering improvements.
- Additional fixes for gameplay mechanics and interface behavior.
- Investigation of missing features documented in the original manuals.
- Restoring selected functionality from the Atari ST, Amiga, or DOS versions where technically feasible.
- Exploring the possibility of adapting the additional Amiga levels for the Genesis version.
- Expanding the accompanying ROM analysis and level-viewing tools.

These are ambitions, not promises. The project will develop according to what is technically possible, what can be tested reliably, and how much time and enthusiasm I can devote to it.

Most importantly, I want the game to remain recognizably **Corporation**.

## Downloads and installation

This project distributes IPS patches and development tools, **not the original game ROM**.

To play the modified version:

1. Obtain the appropriate original Sega Genesis / Mega Drive ROM from a lawful source.
2. Download the IPS patch from this repository's Releases section when a release is available.
3. Apply the patch using a compatible IPS patching utility.
4. Run the patched ROM using a compatible emulator. Gameplay testing has primarily used Kega Fusion; real-cartridge compatibility has not yet been verified.

Always keep an untouched backup of the original ROM.

The current patch targets the original 1 MiB **Cyber-Cop** ROM with SHA-256:

```text
98838ed8d69349ab64a99e4a4e0ea72843d47b175b69fda36957283932f0aba9
```

Apply each cumulative patch to that original ROM, not to a previously modified build. The resulting ROM is 2 MiB.

Rebuilding the patch from source also requires the **Corporation** ROM used for its regional title graphics, with SHA-256:

```text
226368b1693af2db21bb1cc640b94d5b021c9ff20fcb86207d2b76590503cc98
```

The second ROM is needed by the source builder, not by the player applying a ready-made IPS patch. Keep a backup of SRAM before moving between versions. Emulator save states can contain old code addresses and are not guaranteed to work with a different patch version.

## Companion atlas

The offline Russian/English atlas covers all 16 maps, with item and enemy previews, native interaction-panel renders, code notes, access groups and arrival markers. Revision 35 adds resizable previews and blinking terminals. Default code previews do not reveal the code in a randomized running session; terminal access labels assume a documented route.

This repository contains the atlas source template and research scripts, **not** the generated HTML with embedded game graphics, extracted maps or sprite PNGs. The complete atlas is supplied separately. A browser-side local ROM importer is a proposed next step, not an implemented feature of this revision. See [development notes](DEVELOPMENT.md) for the current reproduction limits.

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

— **Valentin "Valet2" Kozin**, October 2026



