#!/usr/bin/env python3
"""Write themes/kanagawa-<variant>.itermcolors from the shared palette.

Usage: scripts/generate.py [path/to/palette.json]   (default: ../.github/palette.json)
"""
import plistlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VARIANTS = ["wave", "dragon", "lotus"]
ANSI = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
# The 16 ANSI colors, normal then bright.
COLORS = [f"term.{c}" for c in ANSI] + [f"term.bright_{c}" for c in ANSI]


def roles(variant):
    """Map each role to its hex color; a role missing from the palette raises KeyError later."""
    return {role: c["hex"] for c in variant["colors"].values() for role in c["usage"]}

def color(h):
    r, g, b = (int(h[i : i + 2], 16) / 255 for i in (1, 3, 5))
    return {
        "Alpha Component": 1.0,
        "Red Component": r,
        "Green Component": g,
        "Blue Component": b,
        "Color Space": "sRGB",
    }


# iTerm2 key -> palette role.
SIMPLE = {
    "Background Color": "ui.bg",
    "Foreground Color": "ui.fg",
    "Bold Color": "ui.fg",
    "Cursor Color": "ui.fg_dim",
    "Cursor Text Color": "ui.bg",
    "Selection Color": "ui.bg_visual",
    "Selected Text Color": "ui.fg",
    "Link Color": "syn.fun",
    "Badge Color": "ui.nontext",
}


def theme(variant, appearance, c):
    d = {f"Ansi {i} Color": color(c[r]) for i, r in enumerate(COLORS)}
    d |= {k: color(c[r]) for k, r in SIMPLE.items()}
    return plistlib.dumps(d)


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / ".github" / "palette.json"
    variants = json.loads(path.read_text())["variants"]
    for v in VARIANTS:
        out = ROOT / "themes" / f"kanagawa-{v}.itermcolors"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(theme(v, variants[v]["appearance"], roles(variants[v])))
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
