#!/usr/bin/env python3
"""
sort.py — Sort files in a directory into subfolders by file type.

Usage:
    python sort.py <directory>           # Sort files (asks for confirmation)
    python sort.py <directory> --dry-run # Preview without moving anything
    python sort.py <directory> --yes     # Sort without confirmation prompt
    python sort.py <directory> --flat    # Use extension names instead of categories
"""

import argparse
import shutil
import sys
from collections import defaultdict
from pathlib import Path

# Map of category name -> set of extensions (lowercase, no dot)
CATEGORIES = {
    "Images":     {"jpg", "jpeg", "png", "gif", "bmp", "webp", "svg", "ico", "tiff", "tif", "heic", "raw", "cr2", "nef", "avif"},
    "Videos":     {"mp4", "mkv", "avi", "mov", "wmv", "flv", "webm", "m4v", "mpg", "mpeg", "3gp", "ts"},
    "Audio":      {"mp3", "wav", "flac", "aac", "ogg", "m4a", "wma", "opus", "aiff", "mid", "midi"},
    "Documents":  {"pdf", "doc", "docx", "odt", "rtf", "txt", "md", "tex", "pages", "wpd"},
    "Spreadsheets": {"xls", "xlsx", "ods", "csv", "tsv", "numbers"},
    "Slides":     {"ppt", "pptx", "odp", "key"},
    "Archives":   {"zip", "tar", "gz", "bz2", "xz", "7z", "rar", "zst", "lz4", "iso", "dmg"},
    "Code":       {"py", "js", "ts", "jsx", "tsx", "html", "css", "scss", "sass", "json", "yaml", "yml",
                   "toml", "xml", "sh", "bash", "zsh", "ps1", "bat", "cmd", "c", "cpp", "h", "hpp",
                   "java", "kt", "cs", "go", "rs", "rb", "php", "swift", "r", "m", "pl", "lua", "vim"},
    "Data":       {"db", "sqlite", "sqlite3", "sql", "parquet", "feather", "pkl", "pickle", "npy", "npz", "hdf5", "h5"},
    "Fonts":      {"ttf", "otf", "woff", "woff2", "eot"},
    "Executables": {"exe", "msi", "app", "deb", "rpm", "apk", "pkg"},
    "3D":         {"obj", "fbx", "stl", "blend", "dae", "glb", "gltf", "3ds", "ply"},
}

# Reverse lookup: extension -> category
EXT_TO_CATEGORY = {ext: cat for cat, exts in CATEGORIES.items() for ext in exts}


def get_destination(file: Path, flat: bool) -> str:
    ext = file.suffix.lstrip(".").lower()
    if flat:
        return ext.upper() if ext else "No Extension"
    return EXT_TO_CATEGORY.get(ext, f"Other ({ext.upper()})" if ext else "No Extension")


def plan_moves(directory: Path, flat: bool) -> list[tuple[Path, Path]]:
    moves = []
    for item in sorted(directory.iterdir()):
        if not item.is_file():
            continue
        folder_name = get_destination(item, flat)
        dest_dir = directory / folder_name
        dest = dest_dir / item.name
        if dest != item:
            moves.append((item, dest))
    return moves


def print_preview(moves: list[tuple[Path, Path]], directory: Path) -> None:
    if not moves:
        print("Nothing to move — directory is already sorted or empty.")
        return

    by_dest: dict[str, list[str]] = defaultdict(list)
    for src, dest in moves:
        by_dest[dest.parent.name].append(src.name)

    print(f"\nWill move {len(moves)} file(s) into {len(by_dest)} folder(s):\n")
    for folder in sorted(by_dest):
        files = by_dest[folder]
        print(f"  {folder}/  ({len(files)} file{'s' if len(files) != 1 else ''})")
        for name in files[:5]:
            print(f"    {name}")
        if len(files) > 5:
            print(f"    ... and {len(files) - 5} more")
    print()


def do_moves(moves: list[tuple[Path, Path]]) -> None:
    for src, dest in moves:
        dest.parent.mkdir(parents=True, exist_ok=True)
        # Avoid clobbering: append a counter if destination already exists
        if dest.exists():
            stem, suffix = dest.stem, dest.suffix
            counter = 1
            while dest.exists():
                dest = dest.parent / f"{stem} ({counter}){suffix}"
                counter += 1
        shutil.move(str(src), str(dest))
    print(f"Done. Moved {len(moves)} file(s).")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sort files in a directory into subfolders by file type.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("directory", help="Directory to sort")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Preview without moving anything")
    parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation prompt")
    parser.add_argument("--flat", action="store_true", help="Use extension names instead of categories (e.g. PNG/, MP3/)")
    args = parser.parse_args()

    directory = Path(args.directory).expanduser().resolve()

    if not directory.exists():
        print(f"Error: '{directory}' does not exist.", file=sys.stderr)
        sys.exit(1)
    if not directory.is_dir():
        print(f"Error: '{directory}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    moves = plan_moves(directory, flat=args.flat)
    print_preview(moves, directory)

    if not moves:
        return

    if args.dry_run:
        print("Dry run — no files were moved.")
        return

    if not args.yes:
        try:
            answer = input("Proceed? [y/N] ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nAborted.")
            return
        if answer not in ("y", "yes"):
            print("Aborted.")
            return

    do_moves(moves)


if __name__ == "__main__":
    main()
