# Nookery Mods

**Five optional quality-of-life mods for Nookery, the Animal Crossing (GameCube) PC port.**

![AI-assisted](https://img.shields.io/badge/AI--assisted-Claude%20Code-blueviolet) ![licence MIT](https://img.shields.io/badge/licence-MIT-blue)

Each mod is off by default, or matches the original game, until you turn it on. A build with all five behaves like plain Nookery until you change a setting.

## The mods

| Mod | What it does | Where to turn it on |
|---|---|---|
| Mouse Glove | Size, flip, rotation, click point, back-of-glove view with a tilt click, click speed, idle hiding, and using the glove in menus. Also fixes the glove blinking while you walk, and Print Screen or modifier keys hiding it. | Controls, Device, Options (Show Back of Glove, Glove in Menus); everything else in config.json |
| Audio Mutes | Separate mutes for music, sound effects and villager voices, each with a hotkey, and small icons in the lower left while muted. | Settings, Audio, Mute; hotkeys under Controls, Keyboard, Hotkeys |
| Instant Text | Text boxes appear all at once while the villager keeps speaking at the normal pace, cut off when you move on. Optional: skip every timed pause. | Settings, Gameplay |
| Save and Quit | A hotkey that opens the gyroid's save screen while you're outdoors in your own town. | Controls, Keyboard, Hotkeys |
| Right-Click Aim | Right-click turns your character toward the mouse cursor before interacting. | Controls, Device, Options |

## Download and install (Windows)

Nookery has no mod loader, so the mods are compiled into Nookery.exe. The release zip contains a Nookery build with all five mods, built from Nookery commit 79f870a (2 November 2026). Use it with that Nookery release: an exe from one version may not match another version's res folder.

1. Download the zip from the Releases page.
2. Close Nookery.
3. Copy your current Nookery.exe, libpng16.dll, zlib1.dll and res folder somewhere safe.
4. Extract the zip over your Nookery folder, letting it replace those files. It adds new files to res and changes none of the existing ones.
5. In Nookery's Settings, turn off the update check, or the updater will replace this build with the official one.

To uninstall, put your saved copies back. Your saves and config.json are not touched; the mod settings in config.json are simply ignored by an unmodded Nookery.

## Config keys

All settings live in config.json in your Nookery data folder. Defaults are shown; they match the original game.

| Key | Default | Meaning |
|---|---|---|
| input.cursorSize | 64 | Glove height, in 480-line game units (16 to 192) |
| input.cursorFlipX | false | Mirror the glove left to right |
| input.cursorFlipY | false | Mirror the glove top to bottom |
| input.cursorRotation | 0 | Degrees clockwise, turned about the click point |
| input.cursorShiftX | 0 | Moves the click point within the glove picture, percent of its size |
| input.cursorShiftY | 0 | Same, downwards |
| input.cursorTurnOver | false | Show the back of the glove; clicks tilt it into the world |
| input.cursorClickTilt | -45 | Tilt angle for that click; flip the sign to tilt the other way |
| input.cursorClickSpeed | 100 | Click animation speed, percent |
| input.cursorHideSeconds | 5 | Hide the glove after this many idle seconds; 0 never hides it |
| input.cursorInMenus | false | Use the glove as the menu pointer too |
| audio.muteMusic, audio.muteSfx, audio.muteVoice | false | The three mutes |
| audio.muteMusicKey, audio.muteSfxKey, audio.muteVoiceKey | none | Hotkeys, by key name such as F6 |
| audio.showMuteIcons | true | Show the lower-left icons while something is muted |
| gameplay.instantText | false | Instant Text |
| gameplay.skipTextPauses | false | Skip every timed pause, including before self-clearing pages |
| input.saveQuitKey | none | Save and Quit hotkey |
| input.rightClickFaceCursor | false | Right-Click Aim |

A back-of-glove setup that points to the top left at half size: cursorSize 32, cursorTurnOver true, cursorRotation -6, cursorShiftX 4, cursorShiftY -82, cursorClickTilt -45. The shift values were measured at 2560 by 1440 and may need small changes on other setups.

## For modders: build your own combination

The patches folder holds the source changes against Nookery commit 79f870a:

- 0000-mod-framework.patch: a small framework the mods share
- 0001-mod-mouse-glove.patch
- 0002-mod-audio-mutes.patch
- 0003-mod-instant-text.patch
- 0004-mod-save-quit.patch
- 0005-mod-right-click-aim.patch

Each mod keeps its code, strings (pc/res/lang/mods) and styles (pc/res/rml/mods) in its own files and registers itself through pc/include/acgc/mods.hpp, so any combination applies without conflicts.

1. Clone flyngmt/ACGC-PC-Port with its submodules and check out commit 79f870a.
2. Apply the framework first: git apply patches/0000-mod-framework.patch
3. Apply any of the mod patches you want, in any order.
4. Build as described in Nookery's BUILDING.md.

To write your own mod, add a file under pc/src/mods that calls ACGC_REGISTER_MOD; the comments in pc/include/acgc/mods.hpp describe the hooks for settings, menu options, hotkeys and overlays.

## Credits and licence

Nookery is by FlyingMeta and contributors, built on the ac-decomp decompilation by ACreTeam. These mods are MIT-licensed (see LICENSE); Nookery's own licence notice is in THIRD_PARTY_NOTICES.md and must go with any build you share. No game files are included: Nookery loads them from your own disc image.
