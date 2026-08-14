"""Turn one high-resolution image into the homepage backdrop set.

    uv run poe backdrop ~/Downloads/wallhaven-xxxxxx.jpg

Writes four files into docs/assets/images/home/:

    backdrop-wide.avif    2560x1440   landscape, for the desktop hero
    backdrop-wide.webp    2560x1440   fallback for anything without AVIF
    backdrop-narrow.avif  1170x2100   a real portrait crop, not a scaled copy
    backdrop-narrow.webp  1170x2100
    backdrop-source.<ext>             the untouched original, kept for re-cropping

The source is listed under exclude_docs in mkdocs.yml, so it lives in the repo
but is never copied into the built site.

The narrow pair is art direction: a phone in portrait shows roughly a third of
the width of a 16:9 frame, so scaling the wide image down would put the subject
off-screen. --focus picks which part of the frame survives that crop, and
--zoom creates pan slack in the wide crop when the source is already 16:9.

Then uncomment the backdrop block in mkdocs.yml.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from PIL import Image

OUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "assets" / "images" / "home"

# Wide covers 2x on a 1280pt-wide layout; narrow covers 3x on a 390pt phone.
WIDE = (2560, 1440)
NARROW = (1170, 2100)

# Fixed by the social plugin. 1.905:1 is wider than 16:9, so it needs its own
# crop rather than letting the plugin cut wherever it likes.
SOCIAL = (1200, 630)

# Baked in: the plugin composites a flat image, so legibility has to be in the
# pixels. One flat wash — shading per text box reads as blobs. 0.62 is the
# measured floor for AA; 0.65 leaves headroom for a different image.
SOCIAL_SCRIM_COLOUR = (13, 14, 22)
SOCIAL_SCRIM = 0.65

# AVIF at this quality is visually lossless for a backdrop sitting behind a
# dimming wash. WebP needs a little more to avoid banding in gradients.
AVIF_QUALITY = 62
WEBP_QUALITY = 82


def crop_to(
    img: Image.Image, size: tuple[int, int], focus: float, zoom: float = 1.0
) -> Image.Image:
    """Cover-crop to `size`, keeping `focus` (0..1) of the trimmed axis in frame.

    `zoom` > 1 takes a tighter window than strictly necessary, which is what
    creates slack for `focus` to pan into. Without it a source that already
    matches the output aspect has nothing to trim, so `focus` does nothing —
    which is the case for any 16:9 wallpaper feeding the 16:9 wide crop.
    """
    target = size[0] / size[1]
    source = img.width / img.height

    if source > target:
        keep_w = round(img.height * target)
        keep_h = img.height
    else:
        keep_w = img.width
        keep_h = round(img.width / target)

    keep_w = min(img.width, round(keep_w / zoom))
    keep_h = min(img.height, round(keep_h / zoom))

    left = round((img.width - keep_w) * focus)
    top = round((img.height - keep_h) * focus)
    box = (left, top, left + keep_w, top + keep_h)

    return img.resize(size, Image.LANCZOS, box=box)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source", type=Path, help="high-resolution source image")
    ap.add_argument(
        "--narrow-source",
        type=Path,
        help="separate image for the phone crop. Cutting a 1170x2100 sliver out "
        "of a landscape frame often decapitates the subject; a purpose-made "
        "portrait wallpaper avoids that. Defaults to the main source.",
    )
    ap.add_argument(
        "--zoom",
        type=float,
        default=1.0,
        help="crop the WIDE image tighter than necessary (1.0 = no zoom). Needed "
        "for --focus to do anything when the source already matches 16:9.",
    )
    ap.add_argument(
        "--focus",
        type=float,
        default=0.5,
        help="0 = keep the left/top of the frame, 1 = keep the right/bottom "
        "(default 0.5, centred). Only affects the axis being trimmed.",
    )
    args = ap.parse_args()

    if not 0.0 <= args.focus <= 1.0:
        print("--focus must be between 0 and 1", file=sys.stderr)
        return 1

    sources = {"wide": args.source, "narrow": args.narrow_source or args.source}
    images: dict[str, Image.Image] = {}

    for name, path in sources.items():
        if not path.is_file():
            print(f"no such file: {path}", file=sys.stderr)
            return 1
        if path not in {p for p in images}:
            images[name] = Image.open(path).convert("RGB")

    for name, img in images.items():
        print(f"source ({name:>6})  {sources[name].name}  {img.width}x{img.height}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for name, size in (("wide", WIDE), ("narrow", NARROW)):
        img = images[name]
        # Wide only: the narrow crop already discards two thirds of a
        # landscape frame, and zooming would push it under 1170px.
        zoom = args.zoom if name == "wide" else 1.0
        frame = crop_to(img, size, args.focus, zoom)
        scale = min(img.width / size[0], img.height / size[1]) / zoom
        if scale < 1.0:
            print(
                f"warning: {name} crop is upscaled ({scale:.2f}x) and will look "
                f"soft — source needs to be at least {size[0]}x{size[1]}"
                + (", and >=2100px tall for the phone crop" if name == "narrow" else ""),
                file=sys.stderr,
            )
        for ext, kwargs in (
            ("avif", {"quality": AVIF_QUALITY}),
            ("webp", {"quality": WEBP_QUALITY, "method": 6}),
        ):
            path = OUT_DIR / f"backdrop-{name}.{ext}"
            frame.save(path, **kwargs)
            kb = path.stat().st_size / 1024
            print(f"  {path.relative_to(OUT_DIR.parents[3])}  {size[0]}x{size[1]}  {kb:.0f} KB")

    card = crop_to(images["wide"], SOCIAL, args.focus, args.zoom)
    card = Image.blend(card, Image.new("RGB", SOCIAL, SOCIAL_SCRIM_COLOUR), SOCIAL_SCRIM)
    card_path = OUT_DIR / "backdrop-social.png"
    card.save(card_path)
    print(f"  {card_path.relative_to(OUT_DIR.parents[3])}  {SOCIAL[0]}x{SOCIAL[1]}  "
          f"{card_path.stat().st_size / 1024:.0f} KB  (scrim {SOCIAL_SCRIM:.0%}, flat)")

    # Kept so the crops can be redone later. exclude_docs keeps it out of the
    # built site.
    kept = []
    for suffix, path in (("", args.source), ("-narrow", args.narrow_source)):
        if path is None or (suffix and path == args.source):
            continue
        dst = OUT_DIR / f"backdrop-source{suffix}{path.suffix.lower()}"
        # Re-running from the kept source must be a no-op, not a self-copy.
        if path.resolve() != dst.resolve():
            shutil.copy2(path, dst)
        kept.append(dst)

    if kept:
        print("\nsource kept (in the repo, excluded from the build):")
        for dst in kept:
            mb = dst.stat().st_size / 1024 / 1024
            print(f"  {dst.relative_to(OUT_DIR.parents[3])}  {mb:.1f} MB")
        print(f"\nreproduce this crop with:"
              f"\n  uv run poe backdrop {kept[0].relative_to(OUT_DIR.parents[3])}"
              f" --zoom {args.zoom} --focus {args.focus}")

    print("\nNow set the backdrop block in mkdocs.yml if it isn't already.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
