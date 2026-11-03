# Nookery Mods

**Four optional quality-of-life mods for Nookery, the Animal Crossing (GameCube) PC port.**

![AI-assisted](https://img.shields.io/badge/AI--assisted-Claude%20Code-blueviolet) ![licence MIT](https://img.shields.io/badge/licence-MIT-blue)

Every option is off by default, or matches the original game, until you change it, and every option can be changed from the game's menus.

## The mods

| Mod | What it does | Where its settings are |
|---|---|---|
| Mouse Enhancements | Glove size, mirroring, rotation and click point; a back-of-glove view with a tilt click; click speed; how long before the glove hides; using the glove in menus; right-click turning your character toward the cursor before interacting. Also fixes the glove blinking while you walk, and Print Screen or modifier keys hiding it. | Controls, Device, Options, Mouse Enhancements |
| Audio Mutes | Separate mutes for music, sound effects and villager voices, each with a hotkey, and small icons in the lower left while muted. | Settings, Audio, Mute; hotkeys under Controls, Keyboard, Hotkeys |
| Instant Text | Text boxes appear all at once while the villager keeps speaking at the normal pace, cut off when you move on. Optional: skip every timed pause. | Settings, Gameplay |
| Save and Quit | A hotkey that opens the gyroid's save screen while you're outdoors in your own town. | Controls, Keyboard, Hotkeys |

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

Run it again to change which mods are on, or press Uninstall to restore the official files. Your saves and config.json are never touched; mod settings in config.json are simply ignored by plain Nookery.

The installer also works from a command prompt: install_mods.py --list shows the mod ids, and install_mods.py --game FOLDER --mods mouse_enhancements,instant_text installs a selection without the window.

## Settings

Every option has a control in the game's menus (see the table above). They are saved in config.json in your Nookery data folder, under these keys. Defaults are shown; they match the original game.

| Key | Default | Menu name | Meaning |
|---|---|---|---|
| input.rightClickFaceCursor | false | Right-Click Faces Cursor | Turn toward the cursor before a right-click interacts |
| input.cursorInMenus | false | Glove in Menus | Use the glove as the menu pointer too |
| input.cursorTurnOver | false | Show Back of Glove | Show the back of the glove; clicks tilt it into the world |
| input.cursorSize | 64 | Glove Size | Glove height, in 480-line game units (16 to 192) |
| input.cursorFlipX | false | Mirror Left-Right | Mirror the glove left to right |
| input.cursorFlipY | false | Mirror Top-Bottom | Mirror the glove top to bottom |
| input.cursorRotation | 0 | Glove Rotation | Degrees clockwise, turned about the click point |
| input.cursorShiftX | 0 | Click Point Left-Right | Moves the click point within the glove, percent of its size |
| input.cursorShiftY | 0 | Click Point Up-Down | Same, downwards |
| input.cursorClickTilt | -45 | Click Tilt | Tilt angle for the back-of-glove click; change the sign to tilt the other way |
| input.cursorClickSpeed | 100 | Click Speed | Click animation speed, percent |
| input.cursorHideSeconds | 5 | Hide Glove After | Hide the glove after this many idle seconds; 0 never hides it |
| audio.muteMusic, audio.muteSfx, audio.muteVoice | false | Mute Music, Mute Sound Effects, Mute Villager Voices | The three mutes |
| audio.muteMusicKey, audio.muteSfxKey, audio.muteVoiceKey | none | Hotkeys | Keys that toggle the mutes, by key name such as F6 |
| audio.showMuteIcons | true | Show Mute Icons | Show the lower-left icons while something is muted |
| gameplay.instantText | false | Instant Text | Text boxes appear at once |
| gameplay.skipTextPauses | false | Skip Text Pauses | Skip every timed pause, including before self-clearing pages |
| input.saveQuitKey | none | Hotkeys, Save and Quit | Save and Quit key |

A back-of-glove setup that points to the top left at half size: Glove Size 32, Show Back of Glove on, Glove Rotation -6, Click Point Left-Right 4, Click Point Up-Down -82, Click Tilt -45. The click point values were measured at 2560 by 1440 and may need small changes on other setups.

## For modders: build your own combination

The patches folder holds the source changes against Nookery commit 79f870a:

- 0000-mod-framework.patch: a small framework the mods share
- 0001-mod-mouse-enhancements.patch
- 0002-mod-audio-mutes.patch
- 0003-mod-instant-text.patch
- 0004-mod-save-quit.patch

Each mod keeps its code, strings (pc/res/lang/mods) and styles (pc/res/rml/mods) in its own files and registers itself through pc/include/acgc/mods.hpp, so any combination applies without conflicts.

1. Clone flyngmt/ACGC-PC-Port with its submodules and check out commit 79f870a.
2. Apply the framework first: git apply patches/0000-mod-framework.patch
3. Apply any of the mod patches you want, in any order.
4. Build as described in Nookery's BUILDING.md.

A build made this way switches on every mod it contains. To switch some off without rebuilding, put a mods.json next to Nookery.exe listing the ones to keep, in the form {"enabled": ["mouse_enhancements", "instant_text"]}.

To write your own mod, add a file under pc/src/mods that calls ACGC_REGISTER_MOD; the comments in pc/include/acgc/mods.hpp describe the hooks for settings, menu options, hotkeys and overlays.

## Credits and licence

Nookery is by FlyingMeta and contributors, built on the ac-decomp decompilation by ACreTeam. These mods are MIT-licensed (see LICENSE); Nookery's own licence notice is in THIRD_PARTY_NOTICES.md and must go with any build you share. No game files are included: Nookery loads them from your own disc image.
