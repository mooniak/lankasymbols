#!/usr/bin/env python3
"""Split a scanned page into separate motif crops, ready for image_to_glyph.py.

Many scans contain several distinct motifs/borders per page. This detects
them automatically: binarize -> dilate ink to merge nearby strokes into
blobs -> connected-component label -> keep components above a minimum size
-> crop each (with padding) to its own image file.

Usage:
    .venv-imgtools/bin/python3 scripts/segment_page.py images/IMG_2484.HEIC \
        --out crops/ [--min-area-frac 0.01] [--pad 15] [--dilate 12] \
        [--ink-threshold 150] [--preview]

--preview writes an annotated overview PNG (boxes drawn) instead of/in
addition to the crops, so you can sanity check before running the full
batch over many pages.
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageOps
from scipy import ndimage

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pillow_heif = None


def ink_mask(img: Image.Image, threshold: int) -> np.ndarray:
    gray = ImageOps.exif_transpose(img).convert("L")
    gray = ImageOps.autocontrast(gray, cutoff=1)
    arr = np.asarray(gray)
    return arr < threshold


def find_components(mask: np.ndarray, dilate: int, min_area_frac: float,
                     min_dim_frac: float = 0.03):
    structure = np.ones((dilate, dilate), dtype=bool)
    merged = ndimage.binary_dilation(mask, structure=structure)
    labeled, n = ndimage.label(merged)
    h, w = mask.shape
    page_area = h * w
    boxes = []
    for i in range(1, n + 1):
        ys, xs = np.where(labeled == i)
        if ys.size == 0:
            continue
        y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
        area = ys.size  # ink+dilation pixel count, rough proxy
        if area < page_area * min_area_frac:
            continue
        # use the *original* (undilated) mask bbox so crops hug the real ink,
        # and so the min-dimension filter isn't fooled by dilation padding
        orig_ys, orig_xs = np.where(mask[y0:y1 + 1, x0:x1 + 1])
        if orig_ys.size == 0:
            continue
        ry0, ry1 = orig_ys.min() + y0, orig_ys.max() + y0
        rx0, rx1 = orig_xs.min() + x0, orig_xs.max() + x0
        box_h, box_w = ry1 - ry0, rx1 - rx0
        if box_h < h * min_dim_frac or box_w < w * min_dim_frac:
            continue
        boxes.append((ry0, ry1, rx0, rx1))
    boxes.sort(key=lambda b: (b[0], b[2]))
    return boxes


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("images", nargs="+", type=Path)
    ap.add_argument("--out", type=Path, default=Path("crops"))
    ap.add_argument("--ink-threshold", type=int, default=150)
    ap.add_argument("--dilate", type=int, default=25, help="structuring element size for merging nearby strokes")
    ap.add_argument("--min-area-frac", type=float, default=0.01, help="drop components smaller than this fraction of page area")
    ap.add_argument("--min-dim-frac", type=float, default=0.03, help="drop components narrower/shorter than this fraction of page width/height")
    ap.add_argument("--pad", type=int, default=12, help="pixels of whitespace padding added around each crop")
    ap.add_argument("--preview", action="store_true", help="also save an annotated full-page preview with numbered boxes")
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    images = []
    for p in args.images:
        if p.is_dir():
            images.extend(sorted(x for x in p.iterdir() if x.suffix.lower() in
                                  {".heic", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}))
        else:
            images.append(p)

    for img_path in images:
        img = Image.open(img_path)
        img = ImageOps.exif_transpose(img)
        mask = ink_mask(img, args.ink_threshold)
        boxes = find_components(mask, args.dilate, args.min_area_frac, args.min_dim_frac)
        print(f"{img_path.name}: {len(boxes)} motif(s)")

        if args.preview:
            prev = img.convert("RGB").copy()
            draw = ImageDraw.Draw(prev)
            for i, (y0, y1, x0, x1) in enumerate(boxes):
                draw.rectangle([x0, y0, x1, y1], outline=(255, 0, 0), width=6)
                draw.text((x0 + 8, y0 + 8), str(i), fill=(255, 0, 0))
            prev.thumbnail((1400, 1400))
            prev.save(args.out / f"{img_path.stem}_preview.png")

        w, h = img.size
        for i, (y0, y1, x0, x1) in enumerate(boxes):
            cy0, cy1 = max(0, y0 - args.pad), min(h, y1 + args.pad)
            cx0, cx1 = max(0, x0 - args.pad), min(w, x1 + args.pad)
            crop = img.crop((cx0, cy0, cx1, cy1))
            out_path = args.out / f"{img_path.stem}_m{i:02d}.png"
            crop.save(out_path)
            print(f"  -> {out_path} ({crop.size[0]}x{crop.size[1]})")


if __name__ == "__main__":
    main()
