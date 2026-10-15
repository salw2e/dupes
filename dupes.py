import argparse
import shutil
import sys
from pathlib import Path

import imagehash
from PIL import Image

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tiff", ".heic", ".heif"}
TRASH = ".dupes-trash"


def scan(folder):
    photos = []
    for path in sorted(folder.rglob("*")):
        if path.suffix.lower() not in EXTS or TRASH in path.parts or not path.is_file():
            continue
        try:
            with Image.open(path) as im:
                photos.append((path, imagehash.phash(im), im.width * im.height))
        except Exception as e:
            print(f"skip {path}: {e}", file=sys.stderr)
    return photos


# ponytail: compares every photo against every group, slow past ~50k photos; use a BK-tree then
def group(photos, threshold):
    groups = []
    for photo in photos:
        for g in groups:
            if photo[1] - g[0][1] <= threshold:
                g.append(photo)
                break
        else:
            groups.append([photo])
    best = lambda p: (p[2], p[0].stat().st_size)
    return [sorted(g, key=best, reverse=True) for g in groups if len(g) > 1]


def main():
    ap = argparse.ArgumentParser(description="Find duplicate photos, even resized or re-saved ones.")
    ap.add_argument("folder", type=Path)
    ap.add_argument("-t", "--threshold", type=int, default=6, help="how different two photos may be, 0 = identical (default 6)")
    ap.add_argument("--clean", action="store_true", help=f"move the extra copies into FOLDER/{TRASH}")
    args = ap.parse_args()

    folder = args.folder.resolve()
    if not folder.is_dir():
        sys.exit(f"not a folder: {folder}")

    photos = scan(folder)
    groups = group(photos, args.threshold)
    extras = [p for g in groups for p in g[1:]]

    for i, g in enumerate(groups, 1):
        print(f"\ngroup {i}")
        for j, (path, _, px) in enumerate(g):
            print(f"  {'keep' if j == 0 else 'dupe'}  {path.relative_to(folder)}  ({px / 1e6:.1f} MP)")

    size = sum(p[0].stat().st_size for p in extras)
    print(f"\n{len(photos)} photos, {len(groups)} groups, {len(extras)} extra copies ({size / 1e6:.1f} MB)")

    if not args.clean or not extras:
        if extras:
            print("run again with --clean to move the extra copies aside")
        return

    if input(f"move {len(extras)} files to {folder / TRASH}? [y/N] ").strip().lower() != "y":
        return
    for path, _, _ in extras:
        dest = folder / TRASH / path.relative_to(folder)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(path, dest)
    print(f"done, check {folder / TRASH} and delete it when happy")


if __name__ == "__main__":
    main()
