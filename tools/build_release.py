"""Assembles the Nookery Mods release: installer, payload with manifest, docs, and a zip.

Usage: python tools/build_release.py --version 1.0.0 --source D:/GAMES/_MODDING/Nookery-src
           --official D:/path/to/official/files [--out release]

--source is a Nookery checkout on the all-mods branch, already built with the windows-msvc-relwithdebinfo preset.
--official holds the official Nookery.exe, libpng16.dll and zlib1.dll of the matching Nookery release; only their
hashes are recorded, so the installer can recognise an untouched install.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
NOOKERY_REVISION = "79f870a30b2f0743994d2ba2ead22e8f1c1e55f7"
REPLACED_FILES = ["Nookery.exe", "libpng16.dll", "zlib1.dll"]
MODS = [
    {"id": "mouse_enhancements", "name": "Mouse Enhancements",
     "description": "Glove size, flip, rotation, back-of-glove view and click options, the glove in menus, "
                    "right-click turning you toward the cursor, and fixes for the glove blinking or hiding."},
    {"id": "audio_mutes", "name": "Audio Mutes",
     "description": "Separate mutes for music, sound effects and villager voices, with hotkeys and status icons."},
    {"id": "instant_text", "name": "Instant Text",
     "description": "Text boxes appear at once while the villager keeps speaking; optionally skip timed pauses."},
    {"id": "save_quit", "name": "Save and Quit",
     "description": "A hotkey that opens the gyroid's save screen while you're outdoors in your own town."},
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--official", required=True, type=Path)
    parser.add_argument("--out", default=REPO / "release", type=Path)
    args = parser.parse_args()

    branch = subprocess.run(["git", "-C", str(args.source), "branch", "--show-current"], capture_output=True,
                            text=True, check=True).stdout.strip()
    if branch != "all-mods":
        raise SystemExit(f"{args.source} is on {branch}, not all-mods")

    bin_dir = args.source / "build" / "windows-msvc-relwithdebinfo" / "bin"
    name = f"Nookery-Mods-{args.version}"
    stage = args.out / name
    if stage.exists():
        shutil.rmtree(stage)
    payload = stage / "payload"

    files = {}
    for relative in REPLACED_FILES:
        target = payload / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(bin_dir / relative, target)
        files[relative] = sha256(target)
    for pattern in ("res/lang/mods/*.json", "res/rml/mods/*.rcss"):
        for source in sorted((args.source / "pc").glob(pattern)):
            relative = source.relative_to(args.source / "pc").as_posix()
            target = payload / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            files[relative] = sha256(target)

    # Record this build so later releases can recognise and upgrade it.
    known_path = REPO / "tools" / "known_builds.json"
    known = json.loads(known_path.read_text(encoding="utf-8"))
    if files["Nookery.exe"] not in known["modded_exe_sha256"]:
        known["modded_exe_sha256"].append(files["Nookery.exe"])
        known_path.write_text(json.dumps(known, indent=2) + "\n", encoding="utf-8")

    manifest = {
        "version": args.version,
        "nookery_revision": NOOKERY_REVISION,
        "official": {relative: sha256(args.official / relative) for relative in REPLACED_FILES},
        "files": files,
        "earlier_modded_exe": [h for h in known["modded_exe_sha256"] if h != files["Nookery.exe"]],
        "mods": MODS,
    }
    (payload / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    for doc in ("README.md", "LICENSE", "THIRD_PARTY_NOTICES.md"):
        shutil.copy2(REPO / doc, stage / doc)
    shutil.copy2(REPO / "installer" / "install_mods.py", stage / "install_mods.py")
    shutil.copy2(REPO / "installer" / "Install Nookery Mods.bat", stage / "Install Nookery Mods.bat")

    zip_path = args.out / f"{name}.zip"
    zip_path.unlink(missing_ok=True)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(stage.rglob("*")):
            if path.is_file():
                archive.write(path, Path(name) / path.relative_to(stage))
    print(f"{zip_path} ({zip_path.stat().st_size} bytes), {len(files)} payload files")


if __name__ == "__main__":
    main()
