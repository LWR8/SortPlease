# SortPlease

A command-line script that sorts files in a folder into subfolders organised by file type.

## Requirements

Python 3.10 or later. No third-party packages needed — only the standard library.

## Usage

```
python sort.py <directory> [options]
```

### Options

| Flag | Short | Description |
|------|-------|-------------|
| `--dry-run` | `-n` | Preview what would happen without moving any files |
| `--yes` | `-y` | Skip the confirmation prompt and move immediately |
| `--flat` | | Use raw extension names as folder names instead of categories |

### Examples

**Preview before committing:**
```
python sort.py C:\Users\you\Downloads --dry-run
```

**Sort with a confirmation prompt:**
```
python sort.py C:\Users\you\Downloads
```

**Sort without being asked:**
```
python sort.py C:\Users\you\Downloads --yes
```

**Use extension-based folders instead of categories:**
```
python sort.py C:\Users\you\Downloads --flat
```

The `--flat` flag creates folders like `JPG/`, `MP3/`, `PDF/` rather than `Images/`, `Audio/`, `Documents/`.

---

## How it works

1. **Scan** — the script lists every file directly inside the target directory (subfolders are left untouched).
2. **Plan** — each file's extension is looked up in a built-in category map to decide which subfolder it belongs in.
3. **Preview** — a summary is printed showing exactly which files will move and where.
4. **Confirm** — unless `--yes` is passed, you are asked to confirm before anything is changed.
5. **Move** — files are moved using `shutil.move`. If a file with the same name already exists in the destination, a counter is appended (`file (1).jpg`, `file (2).jpg`, …) so nothing is ever overwritten.

### Category map

| Folder | Extensions |
|--------|-----------|
| Images | jpg, jpeg, png, gif, bmp, webp, svg, ico, tiff, heic, raw, cr2, nef, avif |
| Videos | mp4, mkv, avi, mov, wmv, flv, webm, m4v, mpg, mpeg, 3gp, ts |
| Audio | mp3, wav, flac, aac, ogg, m4a, wma, opus, aiff, mid, midi |
| Documents | pdf, doc, docx, odt, rtf, txt, md, tex, pages, wpd |
| Spreadsheets | xls, xlsx, ods, csv, tsv, numbers |
| Slides | ppt, pptx, odp, key |
| Archives | zip, tar, gz, bz2, xz, 7z, rar, zst, lz4, iso, dmg |
| Code | py, js, ts, jsx, tsx, html, css, json, yaml, sh, c, cpp, go, rs, java, and more |
| Data | db, sqlite, sql, parquet, pkl, npy, hdf5, and more |
| Fonts | ttf, otf, woff, woff2, eot |
| Executables | exe, msi, app, deb, rpm, apk, pkg |
| 3D | obj, fbx, stl, blend, dae, glb, gltf, 3ds, ply |

Files with an unrecognised extension are placed in `Other (EXT)/` (e.g. `Other (XYZ)/`). Files with no extension go into `No Extension/`.

### Customising categories

The category map lives at the top of [sort.py](sort.py) in the `CATEGORIES` dictionary. Add or remove extensions from any category, or add a new category key, and the script will pick it up automatically.
