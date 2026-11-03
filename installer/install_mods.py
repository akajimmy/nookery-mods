"""Nookery Mods installer.

Patches an existing Nookery install in place: checks that the game is the Nookery version this release was built
for, backs up every file it will replace (and verifies the copies), installs the modded Nookery.exe and the mods'
resource files, and writes mods.json with the mods you picked. Run it again to change the selection or to uninstall.

Usage:
    python install_mods.py                      opens a window
    python install_mods.py --game DIR --mods mouse_glove,instant_text
    python install_mods.py --game DIR --uninstall
    python install_mods.py --game DIR --status
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAYLOAD = HERE / "payload"
MANIFEST_PATH = PAYLOAD / "manifest.json"
BACKUP_DIR_NAME = "nookery-mods-backup"
MODS_JSON = "mods.json"


class InstallError(Exception):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def load_manifest() -> dict:
    try:
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise InstallError(f"Could not read {MANIFEST_PATH}: {error}") from error


def game_running() -> bool:
    try:
        output = subprocess.run(["tasklist", "/FI", "IMAGENAME eq Nookery.exe", "/NH"], capture_output=True,
                                text=True, check=False).stdout
    except OSError:
        return False
    return "Nookery.exe" in output


class Game:
    """An install folder and what state it is in relative to this release."""

    def __init__(self, folder: Path, manifest: dict):
        self.folder = folder
        self.manifest = manifest
        self.backup_root = folder / BACKUP_DIR_NAME
        self.original_dir = self.backup_root / "original"

    def state(self) -> str:
        """'official', 'modded' (this release), 'missing' or 'unknown'."""
        exe = self.folder / "Nookery.exe"
        if not exe.is_file():
            return "missing"
        digest = sha256(exe)
        if digest == self.manifest["official"]["Nookery.exe"]:
            return "official"
        if digest == self.manifest["files"]["Nookery.exe"]:
            return "modded"
        return "unknown"

    def revision(self) -> str:
        """The source revision Nookery stamps into its exe, for error messages."""
        data = (self.folder / "Nookery.exe").read_bytes()
        marker = data.find(b"Revision:")
        if marker < 0:
            return "unknown"
        return data[marker + 9:marker + 80].split(b"\0")[0].decode("ascii", "replace").strip().split()[0]

    def enabled_mods(self) -> list[str]:
        path = self.folder / MODS_JSON
        try:
            return list(json.loads(path.read_text(encoding="utf-8")).get("enabled", []))
        except (OSError, ValueError):
            return []


def copy_verified(source: Path, target: Path, expected: str | None = None) -> None:
    """Copy a file and confirm the copy's hash, so a backup only counts once it is proven."""
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    want = expected or sha256(source)
    if sha256(target) != want:
        raise InstallError(f"Copy of {source} to {target} does not match; nothing more was changed.")


def check_ready(game: Game, log) -> str:
    if game_running():
        raise InstallError("Nookery is running. Close it and try again.")
    state = game.state()
    if state == "missing":
        raise InstallError(f"No Nookery.exe in {game.folder}.")
    if state == "unknown":
        revision = game.revision()
        wanted = game.manifest["nookery_revision"]
        if revision.startswith(wanted[:7]):
            raise InstallError(
                f"This Nookery.exe is version {wanted[:7]} but differs from the official release file, so it may be "
                "modified or damaged. Reinstall that Nookery release and try again. Nothing was changed.")
        raise InstallError(
            f"This Nookery.exe is version {revision[:7]}, but these mods were built for {wanted[:7]}. "
            "Nothing was changed.")
    log(f"Found {'the official Nookery' if state == 'official' else 'Nookery with these mods'} "
        f"(revision {game.manifest['nookery_revision'][:7]}).")
    return state


def install(game: Game, selected: list[str], log) -> None:
    manifest = game.manifest
    known = {mod["id"] for mod in manifest["mods"]}
    unknown = [mod for mod in selected if mod not in known]
    if unknown:
        raise InstallError(f"Unknown mods: {', '.join(unknown)}")
    state = check_ready(game, log)

    # Keep the untouched official files once, so uninstall can always restore them.
    if state == "official" and not game.original_dir.exists():
        for name, digest in manifest["official"].items():
            copy_verified(game.folder / name, game.original_dir / name, digest)
        log(f"Backed up the original files to {game.original_dir} and checked them.")

    # Back up every file this run overwrites that is not already identical to the payload.
    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    run_dir = game.backup_root / stamp
    replaced = []
    targets = list(manifest["files"].items()) + [(MODS_JSON, None)]
    for relative, digest in targets:
        current = game.folder / relative
        if current.is_file() and (digest is None or sha256(current) != digest):
            copy_verified(current, run_dir / relative)
            replaced.append(relative)
    if replaced:
        log(f"Backed up {len(replaced)} file(s) that will be replaced to {run_dir} and checked them.")

    # Install the payload, checking each copied file.
    for relative, digest in manifest["files"].items():
        target = game.folder / relative
        if target.is_file() and sha256(target) == digest:
            continue
        copy_verified(PAYLOAD / relative, target, digest)
    (game.folder / MODS_JSON).write_text(json.dumps({"enabled": selected}, indent=2) + "\n", encoding="utf-8")
    names = [mod["name"] for mod in manifest["mods"] if mod["id"] in selected]
    log("Installed. Mods on: " + (", ".join(names) if names else "none (plain Nookery behaviour)") + ".")


def uninstall(game: Game, log) -> None:
    state = check_ready(game, log)
    if state == "official":
        log("Nookery is already the official build; nothing to remove.")
        return
    if not game.original_dir.is_dir():
        raise InstallError(f"No original backup in {game.original_dir}, so the official files can't be restored. "
                           "Nothing was changed.")
    for name, digest in game.manifest["official"].items():
        backup = game.original_dir / name
        if not backup.is_file() or sha256(backup) != digest:
            raise InstallError(f"The backup of {name} is missing or changed; nothing was changed.")
    for name, digest in game.manifest["official"].items():
        copy_verified(game.original_dir / name, game.folder / name, digest)
    for relative in game.manifest["files"]:
        if relative not in game.manifest["official"]:
            (game.folder / relative).unlink(missing_ok=True)
    for folder in ("res/lang/mods", "res/rml/mods"):
        path = game.folder / folder
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()
    (game.folder / MODS_JSON).unlink(missing_ok=True)
    log(f"Restored the official files. Backups are kept in {game.backup_root}.")


def run_cli(args, manifest: dict) -> int:
    game = Game(Path(args.game).resolve(), manifest)
    try:
        if args.status:
            state = game.state()
            print(f"{game.folder}: {state}")
            if state == "modded":
                print("Mods on: " + (", ".join(game.enabled_mods()) or "none"))
        elif args.uninstall:
            uninstall(game, print)
        else:
            selected = [mod for mod in (args.mods or "").split(",") if mod]
            install(game, selected, print)
    except InstallError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


def run_gui(manifest: dict) -> int:
    import tkinter as tk
    from tkinter import filedialog, messagebox, scrolledtext

    root = tk.Tk()
    root.title(f"Nookery Mods {manifest['version']} installer")
    folder = tk.StringVar()
    checks = {mod["id"]: tk.BooleanVar() for mod in manifest["mods"]}

    frame = tk.Frame(root, padx=12, pady=12)
    frame.pack(fill="both", expand=True)
    tk.Label(frame, text="Nookery folder (the one with Nookery.exe):").grid(row=0, column=0, columnspan=2, sticky="w")
    tk.Entry(frame, textvariable=folder, width=60).grid(row=1, column=0, sticky="we")

    log_box = scrolledtext.ScrolledText(frame, height=8, width=80, state="disabled")

    def log(text: str) -> None:
        log_box.configure(state="normal")
        log_box.insert("end", text + "\n")
        log_box.see("end")
        log_box.configure(state="disabled")
        root.update_idletasks()

    def load_folder() -> None:
        path = Path(folder.get())
        if not (path / "Nookery.exe").is_file():
            return
        game = Game(path, manifest)
        state = game.state()
        log(f"{path}: " + {"official": "official Nookery, ready to install",
                           "modded": "Nookery with these mods; change the selection or uninstall",
                           "unknown": f"a Nookery version these mods weren't built for (revision {game.revision()})",
                           }.get(state, state))
        for mod_id, var in checks.items():
            var.set(mod_id in game.enabled_mods())

    def browse() -> None:
        chosen = filedialog.askdirectory(title="Choose your Nookery folder")
        if chosen:
            folder.set(chosen)
            load_folder()

    tk.Button(frame, text="Browse...", command=browse).grid(row=1, column=1, padx=(6, 0))

    tk.Label(frame, text="Mods to switch on:").grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 0))
    row = 3
    for mod in manifest["mods"]:
        tk.Checkbutton(frame, text=mod["name"], variable=checks[mod["id"]], anchor="w").grid(
            row=row, column=0, columnspan=2, sticky="w")
        tk.Label(frame, text=mod["description"], fg="#555", wraplength=520, justify="left").grid(
            row=row + 1, column=0, columnspan=2, sticky="w", padx=(24, 0))
        row += 2

    def act(action, closing_note: str) -> None:
        """Run an install or uninstall; on success show what happened and close, on failure stay open."""
        if not folder.get():
            messagebox.showwarning("Nookery Mods", "Choose your Nookery folder first.")
            return
        messages: list[str] = []

        def record(text: str) -> None:
            messages.append(text)
            log(text)

        try:
            action(Game(Path(folder.get()), manifest), record)
        except InstallError as error:
            log(f"Error: {error}")
            messagebox.showerror("Nookery Mods", str(error))
            return
        summary = messages[-1] if messages else "Done."
        messagebox.showinfo("Nookery Mods", f"{summary}\n\n{closing_note}".strip())
        root.destroy()

    buttons = tk.Frame(frame)
    buttons.grid(row=row, column=0, columnspan=2, sticky="w", pady=10)
    tk.Button(buttons, text="Install / update selection",
              command=lambda: act(
                  lambda game, out: install(game, [m for m, v in checks.items() if v.get()], out),
                  "If you haven't yet, turn off the update check in Nookery's Settings, or the updater will replace "
                  "the modded build.")).pack(side="left")
    tk.Button(buttons, text="Uninstall (restore original)",
              command=lambda: act(lambda game, out: uninstall(game, out), "")).pack(side="left", padx=(8, 0))
    log_box.grid(row=row + 1, column=0, columnspan=2, sticky="we")

    default = HERE.parent
    if (default / "Nookery.exe").is_file():
        folder.set(str(default))
        load_folder()
    root.mainloop()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Nookery Mods into an existing Nookery folder.")
    parser.add_argument("--game", help="Nookery folder (contains Nookery.exe); omit to open the window")
    parser.add_argument("--mods", help="comma-separated mod ids to switch on, e.g. mouse_glove,instant_text")
    parser.add_argument("--uninstall", action="store_true", help="restore the original Nookery files")
    parser.add_argument("--status", action="store_true", help="show what is installed")
    parser.add_argument("--list", action="store_true", help="list the mod ids")
    args = parser.parse_args()
    try:
        manifest = load_manifest()
    except InstallError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    if args.list:
        for mod in manifest["mods"]:
            print(f"{mod['id']:20} {mod['name']}: {mod['description']}")
        return 0
    if args.game:
        return run_cli(args, manifest)
    return run_gui(manifest)


if __name__ == "__main__":
    sys.exit(main())
