#!/usr/bin/env python3
"""Turn a scanned image (motif/border/outline) into a UFO glyph.

Pipeline: image -> cleaned bilevel bitmap -> potrace SVG -> font outline -> .glif

Usage:
    .venv-imgtools/bin/python3 scripts/image_to_glyph.py IMAGE [IMAGE ...] \
        --ufo sources/LankaSymbols.ufo [--name lks-my-motif] [--unicode F700] \
        [--threshold 128] [--invert] [--height 740] [--margin 20] \
        [--turdsize 2] [--opttolerance 0.2] [--keep-debug]

Batch mode: pass a directory or multiple images without --name; each file's
stem (slugified) becomes the glyph name "lks-<slug>".

Requires: potrace on PATH (`brew install potrace`), and the venv at
.venv-imgtools (pillow, pillow-heif, fonttools, numpy) created once via:
    python3 -m venv .venv-imgtools
    .venv-imgtools/bin/pip install pillow pillow-heif fonttools numpy
"""
import argparse
import plistlib
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np
from PIL import Image, ImageOps

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pillow_heif = None

from fontTools.svgLib.path import parse_path
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.pointPen import SegmentToPointPen
from fontTools.ufoLib.glifLib import GlyphSet
from fontTools.misc.transform import Transform

SVG_NS = {"svg": "http://www.w3.org/2000/svg"}


def slugify(stem: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", stem).strip("-").lower()
    return s


def load_and_binarize(image_path: Path, threshold: int, invert: bool, max_dim: int = 1400) -> Image.Image:
    img = Image.open(image_path)
    img = ImageOps.exif_transpose(img)
    img = img.convert("L")
    img = ImageOps.autocontrast(img, cutoff=1)
    if max(img.size) > max_dim:
        # Downsample before tracing: scanned-at-full-resolution source images make
        # potrace emit tens of thousands of curve points (from paper grain/jpeg
        # noise at the pixel level), which overflows a TrueType glyph's point
        # budget. Font outlines don't need more detail than this anyway.
        scale = max_dim / max(img.size)
        img = img.resize((max(1, round(img.width * scale)), max(1, round(img.height * scale))), Image.LANCZOS)
    arr = np.asarray(img)
    mask = arr < threshold  # dark pixels -> ink
    if invert:
        mask = ~mask
    bw = Image.fromarray((~mask * 255).astype(np.uint8))  # potrace: black=1=ink, PBM 0=black
    return bw.convert("1")


def trace_to_svg(bitmap: Image.Image, turdsize: int, opttolerance: float, debug_dir: Path = None) -> str:
    with tempfile.TemporaryDirectory() as td:
        pbm_path = Path(td) / "trace.pbm"
        svg_path = Path(td) / "trace.svg"
        bitmap.save(pbm_path)
        if debug_dir:
            debug_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy(pbm_path, debug_dir / "binarized.pbm")
        subprocess.run(
            [
                "potrace", str(pbm_path), "-s", "-o", str(svg_path),
                "--turdsize", str(turdsize),
                "--opttolerance", str(opttolerance),
                "--flat",
            ],
            check=True, capture_output=True,
        )
        svg_text = svg_path.read_text()
        if debug_dir:
            shutil.copy(svg_path, debug_dir / "traced.svg")
        return svg_text


def svg_to_pen(svg_text: str):
    root = ET.fromstring(svg_text)
    width = float(root.get("width").replace("pt", ""))
    height = float(root.get("height").replace("pt", ""))
    pen = RecordingPen()
    for path_el in root.iter("{http://www.w3.org/2000/svg}path"):
        d = path_el.get("d")
        if d:
            parse_path(d, pen)
    return pen, width, height


def fit_and_write_glyph(pen, svg_w, svg_h, ufo_path: Path, glyph_name: str,
                         unicode_hex: str, target_height: float, margin: float,
                         baseline: float):
    recorded = pen.value
    tmp_pen = RecordingPen()
    tmp_pen.value = recorded
    bounds = _bounds(recorded)
    if bounds is None:
        raise SystemExit("Traced outline is empty — check threshold/invert settings.")
    x0, y0, x1, y1 = bounds
    src_h = y1 - y0
    src_w = x1 - x0
    if src_h <= 0:
        raise SystemExit("Degenerate outline bounds.")
    scale = target_height / src_h
    # SVG y grows downward; flip to font (y-up), then translate into position.
    t = Transform()
    t = t.translate(margin, baseline)
    t = t.scale(scale, -scale)
    t = t.translate(-x0, -y0 - src_h)
    final_pen = RecordingPen()
    tpen = TransformPen(final_pen, t)
    for op, args in recorded:
        getattr(tpen, op)(*args)

    glyph_width = src_w * scale + margin * 2

    glyphset_dir = ufo_path / "glyphs"
    glyphset = GlyphSet(str(glyphset_dir))

    class _Glyph:
        pass

    g = _Glyph()
    g.width = round(glyph_width)
    g.height = None
    g.unicodes = [int(unicode_hex, 16)] if unicode_hex else []
    g.note = None
    g.lib = {}
    g.anchors = []
    g.guidelines = []
    g.image = None

    def draw_points(pointPen):
        final_pen.replay(SegmentToPointPen(pointPen))

    glyphset.writeGlyph(glyph_name, g, drawPointsFunc=draw_points)
    glyphset.writeContents()
    return g.width


def _bounds(recorded):
    xs, ys = [], []
    for op, args in recorded:
        for pt in args:
            if isinstance(pt, tuple):
                xs.append(pt[0])
                ys.append(pt[1])
    if not xs:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def next_free_pua_codepoint(ufo_path: Path, start=0xF700, end=0xFFFD) -> int:
    used = set()
    for glif in (ufo_path / "glyphs").glob("*.glif"):
        text = glif.read_text()
        for m in re.finditer(r'<unicode hex="([0-9A-Fa-f]+)"', text):
            used.add(int(m.group(1), 16))
    cp = start
    while cp in used and cp <= end:
        cp += 1
    if cp > end:
        raise SystemExit("Ran out of free PUA codepoints.")
    return cp


def _point_count(recorded) -> int:
    return sum(len(args) for op, args in recorded if op != "closePath")


# A TrueType simple glyph's point/coordinate data must fit in one loca-table
# delta slot; in practice that caps out well below this, and beyond ~15k points
# fontmake/woff2 compression starts corrupting glyf data (IndexError on decompile).
# Scans of highly detailed engravings (stippled shading, fine hatching) can trace
# to 20k+ points at normal resolution, so retry at progressively lower resolution
# and heavier simplification until the outline fits a safe budget.
MAX_SAFE_POINTS = 6000


def process_one(image_path: Path, ufo_path: Path, name: str, unicode_hex: str,
                 threshold: int, invert: bool, target_height: float, margin: float,
                 baseline: float, turdsize: int, opttolerance: float, max_dim: int,
                 debug_dir: Path = None, max_points: int = MAX_SAFE_POINTS):
    attempt_dim, attempt_turdsize, attempt_opttolerance = max_dim, turdsize, opttolerance
    for attempt in range(6):
        bitmap = load_and_binarize(image_path, threshold, invert, attempt_dim)
        svg_text = trace_to_svg(bitmap, attempt_turdsize, attempt_opttolerance, debug_dir)
        pen, svg_w, svg_h = svg_to_pen(svg_text)
        npoints = _point_count(pen.value)
        if npoints <= max_points or attempt == 5:
            if npoints > max_points:
                print(f"  (warning: {npoints} points even after simplification — "
                      f"glyph may be too complex; consider cropping it smaller)")
            break
        print(f"  {npoints} points is too complex (budget {max_points}); "
              f"simplifying and retracing...")
        attempt_dim = max(150, round(attempt_dim * 0.65))
        attempt_turdsize = round(attempt_turdsize * 1.8) + 2
        attempt_opttolerance = attempt_opttolerance * 1.6 + 0.3
    if unicode_hex is None:
        unicode_hex = f"{next_free_pua_codepoint(ufo_path):04X}"
    width = fit_and_write_glyph(pen, svg_w, svg_h, ufo_path, name, unicode_hex,
                                 target_height, margin, baseline)
    print(f"  -> glyph '{name}' unicode U+{unicode_hex} width={width}")
    return name, unicode_hex


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("images", nargs="+", type=Path, help="image file(s) or a directory of images")
    ap.add_argument("--ufo", type=Path, default=Path("sources/LankaSymbols.ufo"))
    ap.add_argument("--name", help="glyph name (single-image mode only)")
    ap.add_argument("--unicode", help="hex codepoint, e.g. F700 (auto-assigned PUA if omitted)")
    ap.add_argument("--threshold", type=int, default=128, help="0-255 grayscale cutoff for ink")
    ap.add_argument("--invert", action="store_true", help="treat light pixels as ink instead of dark")
    ap.add_argument("--height", type=float, default=740.0, help="target glyph height in font units (default: capHeight)")
    ap.add_argument("--margin", type=float, default=20.0, help="left/right sidebearing in font units")
    ap.add_argument("--baseline", type=float, default=0.0, help="y position of the glyph's baseline-aligned bottom")
    ap.add_argument("--turdsize", type=int, default=2, help="potrace: suppress speckles smaller than this")
    ap.add_argument("--opttolerance", type=float, default=0.2, help="potrace curve-fit tolerance")
    ap.add_argument("--max-dim", type=int, default=1400, help="downsample the source image so its longest side is at most this many pixels before tracing (keeps glyph point counts sane)")
    ap.add_argument("--max-points", type=int, default=MAX_SAFE_POINTS, help="if a trace exceeds this many points, auto-retry at lower resolution/detail until it fits (or 6 attempts are exhausted)")
    ap.add_argument("--keep-debug", action="store_true", help="save intermediate .pbm/.svg next to the image")
    args = ap.parse_args()

    if not (args.ufo / "glyphs" / "contents.plist").exists():
        raise SystemExit(f"Not a UFO glyphs dir: {args.ufo}")

    images = []
    for p in args.images:
        if p.is_dir():
            images.extend(sorted(x for x in p.iterdir() if x.suffix.lower() in
                                  {".heic", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}))
        else:
            images.append(p)

    if args.name and len(images) > 1:
        raise SystemExit("--name only works with a single image; batch mode derives names from filenames.")

    for img_path in images:
        name = args.name or f"lks-{slugify(img_path.stem)}"
        debug_dir = img_path.parent / f".{img_path.stem}-debug" if args.keep_debug else None
        print(f"Processing {img_path} -> {name}")
        process_one(img_path, args.ufo, name, args.unicode, args.threshold, args.invert,
                    args.height, args.margin, args.baseline, args.turdsize, args.opttolerance,
                    args.max_dim, debug_dir, args.max_points)

    print(f"\nDone. {len(images)} glyph(s) written to {args.ufo}/glyphs/")
    print("Review in Glyphs/FontForge, then rebuild with: mnik build (or your usual pipeline).")


if __name__ == "__main__":
    main()
