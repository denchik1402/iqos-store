"""Generate favicon.png (120x120) and favicon.ico from favicon.svg."""
from __future__ import annotations

from pathlib import Path

from PIL import Image
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg


def gen_from_svg(svg_path: Path, out_dir: Path) -> None:
    drawing = svg2rlg(str(svg_path))
    if drawing is None:
        raise RuntimeError(f"Could not parse SVG: {svg_path}")

    png = out_dir / "favicon.png"
    ico = out_dir / "favicon.ico"
    renderPM.drawToFile(drawing, str(png), fmt="PNG", dpi=120)
    img = Image.open(png).convert("RGBA").resize((120, 120), Image.Resampling.LANCZOS)
    img.save(png, format="PNG")
    img.save(ico, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (120, 120)])
    print(f"OK {out_dir} png={png.stat().st_size} ico={ico.stat().st_size}")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    for name in ("iqos-store", "lilsolid-repo", "my_shop_full"):
        svg = root / name / "favicon.svg"
        if svg.exists():
            gen_from_svg(svg, root / name)


if __name__ == "__main__":
    main()
