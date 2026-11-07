# Nookery Mods

**Four optional quality-of-life mods for [Nookery](https://github.com/flyngmt/ACGC-PC-Port), the Animal Crossing (GameCube) PC port by FlyingMeta.**

![AI-assisted](https://img.shields.io/badge/AI--assisted-Claude%20Code-blueviolet) ![licence MIT](https://img.shields.io/badge/licence-MIT-blue)

You choose which mods to install, and every option can be changed from the game's menus. Mods you don't install change nothing.

## The mods

| Mod | What it does | Where its settings are |
|---|---|---|
| Mouse Enhancements | An Enhanced cursor: the back of a smaller glove pointing to the top left, clicking on its fingertip and tilting into the world when you click. Use it out of menus, in menus (replacing the menu hand) or everywhere; keep the cursor from hiding when idle; right-click turns your character toward the cursor before interacting. Also fixes the glove blinking while you walk, and Print Screen or modifier keys hiding it. | Settings, Mouse (a tab that appears when this mod is on) |
| Audio Mutes | Separate mutes for music, sound effects and villager voices, each with a hotkey, and small icons in the lower left while muted. | Settings, Audio, Mute; hotkeys under Controls, Keyboard, Hotkeys |
| Instant Text | Text boxes appear all at once while the villager keeps speaking at the normal pace, cut off when you move on. Optional: skip every timed pause, and show item names in menus without the delay. | Settings, Gameplay |
| Save and Quit | A hotkey that opens the gyroid's save screen while you're outdoors in your own town. Optional: close the game after saving instead of going back to the title screen. | Controls, Keyboard, Hotkeys; Settings, Gameplay |
| Villager Map | The town map marks where each villager is right now, yellow outdoors and white indoors, and names who is in the selected acre. | Settings, Gameplay |
| Relaxed Fishing | Slower nibbles, longer to hook a bite, fish never bite on the first pull, and a sound when one bites. | Settings, Gameplay |

## Screenshots

The Enhanced cursor from Mouse Enhancements:

| In town | In the inventory |
|---|---|
| ![The Enhanced cursor in town](docs/images/cursor-field.png) | ![The Enhanced cursor in the inventory](docs/images/cursor-menu.png) |

Mouse Enhancements adds a Mouse tab to Settings:

![Settings, Mouse tab](docs/images/settings-mouse.png)

Audio Mutes adds a Mute section to Settings, Audio:

![Settings, Audio tab with the Mute section](docs/images/settings-audio.png)

Instant Text adds two options to Settings, Gameplay:

![Settings, Gameplay tab with Instant Text and Skip Text Pauses](docs/images/settings-gameplay.png)

## Download and install (Windows)

The release zip contains an installer that patches your existing Nookery folder in place and lets you pick which mods to switch on. It needs Python 3.9 or newer (from python.org or the Microsoft Store).

1. Download the zip from the Releases page and extract it anywhere, for example into your Nookery folder.
2. Close Nookery.
3. Double-click Install Nookery Mods.bat.
4. Choose your Nookery folder (the one with Nookery.exe), tick the mods you want, and press Install.
5. In Nookery's Settings, turn off the update check, or the updater will replace the modded build with the official one.

What the installer does:

- It checks your Nookery.exe is the version these mods were built for, Nookery commit 79f870a (2 November 2026). With any other version it stops and changes nothing.
- Before replacing anything it copies each file into a nookery-mods-backup folder inside your Nookery folder and checks the copy. The untouched official files are kept in nookery-mods-backup\original.
- It installs a Nookery.exe that contains every mod, the mods' text and style files, and a mods.json listing the mods you ticked. Mods you didn't tick stay switched off and add nothing to the game.

Run it again to change which mods are on, or press Uninstall to restore the official files. To update, run the installer from a newer release: it recognises earlier versions of these mods and replaces them, keeping your selection ticked. Your saves and config.json are never touched; mod settings in config.json are simply ignored by plain Nookery.

The installer also works from a command prompt: install_mods.py --list shows the mod ids, and install_mods.py --game FOLDER --mods mouse_enhancements,instant_text installs a selection without the window.

## Settings

Every option has a control in the game's menus (see the table above). They are saved in config.json in your Nookery data folder, under these keys.

| Key | Default | Menu name | Choices |
|---|---|---|---|
| input.cursorStyle | 1 (Enhanced) | Cursor Style | 0 Vanilla, 1 Enhanced |
| input.cursorScope | 2 (Everywhere) | Show Enhanced Cursor | 0 Out of Menus, 1 In Menus, 2 Everywhere |
| input.cursorHideSeconds | 0 (Never) | Hide Cursor After | 0 never hides the cursor, or 1 to 99 seconds without mouse movement (the original game uses 5) |
| input.rightClickFaceCursor | true | Right-Click Faces Cursor | Turn toward the cursor before a right-click interacts |
| audio.muteMusic, audio.muteSfx, audio.muteVoice | false | Mute Music, Mute Sound Effects, Mute Villager Voices | The three mutes |
| audio.muteMusicKey, audio.muteSfxKey, audio.muteVoiceKey | M, N, V | Hotkeys | Keys that toggle the mutes, by key name |
| audio.showMuteIcons | true | Show Mute Icons | Show the lower-left icons while something is muted |
| gameplay.instantText | false | Instant Text | Text boxes appear at once |
| gameplay.skipTextPauses | false | Skip Text Pauses | Skip every timed pause, including before self-clearing pages |
| gameplay.instantItemNames | false | Instant Item Names | Item names in menus appear with no delay |
| input.saveQuitKey | F5 | Hotkeys, Save and Quit | Save and Quit key |
| gameplay.saveQuitToDesktop | false | Quit to Desktop After Saving | Close the game after saving and ending, from the hotkey or your gyroid |
| gameplay.villagerMap | true | Show Villagers on Map | Mark where each villager is now on the town map |
| gameplay.fishingNibblePercent | 200 | Time Between Nibbles | 100 to 400 percent of the original time between pulls on the bobber |
| gameplay.fishingBiteWindowPercent | 300 | Time to Hook a Bite | 100 to 500 percent of the original time to reel in after a bite |
| gameplay.fishingNoFirstBite | true | Never Bite on First Pull | A fish's first touch on the bobber is always a nibble |
| gameplay.fishingBiteSound | 3 (Splash and Chomp) | Bite Sound | 0 Off, 1 Splash, 2 Chomp, 3 Splash and Chomp |

Hotkeys also reach the game, so a hotkey on a key bound to a game button does both. The default hotkeys are all keys Nookery's default keyboard layout leaves unbound; if you rebind your controls, keep them clear of these.

## For modders: build your own combination

The patches folder holds the source changes against Nookery commit 79f870a:

- 0000-mod-framework.patch: a small framework the mods share
- 0001-mod-mouse-enhancements.patch
- 0002-mod-audio-mutes.patch
- 0003-mod-instant-text.patch
- 0004-mod-save-quit.patch
- 0005-mod-villager-map.patch
- 0006-mod-relaxed-fishing.patch

Each mod keeps its code, strings (pc/res/lang/mods) and styles (pc/res/rml/mods) in its own files and registers itself through pc/include/acgc/mods.hpp, so any combination applies without conflicts.

1. Clone flyngmt/ACGC-PC-Port with its submodules and check out commit 79f870a.
2. Apply the framework first: git apply patches/0000-mod-framework.patch
3. Apply any of the mod patches you want, in any order.
4. Build as described in Nookery's BUILDING.md.

A build made this way switches on every mod it contains. To switch some off without rebuilding, put a mods.json next to Nookery.exe listing the ones to keep, in the form {"enabled": ["mouse_enhancements", "instant_text"]}.

To write your own mod, add a file under pc/src/mods that calls ACGC_REGISTER_MOD; the comments in pc/include/acgc/mods.hpp describe the hooks for settings, menu options, hotkeys and overlays.

## Credits

These mods are small additions to other people's much larger work. All the credit for Animal Crossing running on PC goes to them.

- **[Nookery](https://github.com/flyngmt/ACGC-PC-Port)** by [FlyingMeta](https://github.com/flyngmt) and its [contributors](https://github.com/flyngmt/ACGC-PC-Port/graphs/contributors): the PC port these mods build on. Every mod here is a patch to Nookery's code.
- **[ac-decomp](https://github.com/ACreTeam/ac-decomp)** by [ACreTeam](https://github.com/ACreTeam): the decompilation of Animal Crossing that Nookery is built on. Nookery also credits [Cuyler](https://github.com/Cuyler36) for sharing the code of the Deluxe mod and for help with how the game works.
- **[Aurora](https://github.com/encounter/aurora)** and **[Borealis](https://github.com/encounter/borealis)** by [Encounter (Luke Street)](https://github.com/encounter): the GameCube platform layer and the app framework Nookery runs on, including the settings menus these mods add to.
- **[FixNES](https://github.com/FIX94/fixNES)** by [FIX94](https://github.com/FIX94): the NES emulator inside Nookery.
- Nookery's own credits also thank [Tom Lube](https://github.com/tomlube) for testing, the [Dusklight](https://github.com/TwilitRealm/dusklight) team, [Rainy Ram](https://bsky.app/profile/rainyr.am) for the Nookery icon and in-game signs, YourPalFox for the earlier logo, and the Animal Crossing Modding Discord. See the Credits section of [Nookery's README](https://github.com/flyngmt/ACGC-PC-Port#credits).

Animal Crossing is a trademark of Nintendo. These mods are an unofficial fan project, not affiliated with or endorsed by Nintendo or by the Nookery project.

## Licence

These mods are MIT-licensed (see LICENSE). The release build includes Nookery and the open-source libraries it uses; THIRD_PARTY_NOTICES.md lists each one with its authors and licence, and the licenses folder has every licence in full. Those notices must go with any build you share.

No Nintendo game files are included anywhere in this repository or the release: Nookery loads all game data from your own disc image at runtime. The screenshots show the game running with these mods.
