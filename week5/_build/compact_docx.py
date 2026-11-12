# -*- coding: utf-8 -*-
"""Shrink the image payload inside a DOCX without changing its layout.

The report contains twelve high-resolution PNG figures.  Re-encoding them as
256-colour PNGs preserves the flat chart palette and crisp labels while cutting
the file well below the 2 MB upload ceiling.  Image dimensions are unchanged,
so Word keeps every figure at its designed size.
"""

from __future__ import annotations

import sys
import zipfile
from io import BytesIO
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
DEFAULT_DOCX = HERE.parent / "Agribusiness_Model_Evaluation_Reporting_Strategy_Week5.docx"


def compact_png(data: bytes, colors: int = 256) -> bytes:
    image = Image.open(BytesIO(data))
    if image.mode == "RGBA":
        alpha = image.getchannel("A")
        if alpha.getextrema() == (255, 255):
            image = image.convert("RGB")
        else:
            background = Image.new("RGB", image.size, "white")
            background.paste(image, mask=alpha)
            image = background
    elif image.mode not in ("RGB", "L"):
        image = image.convert("RGB")

    quantized = image.quantize(
        colors=colors,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.FLOYDSTEINBERG,
    )
    output = BytesIO()
    quantized.save(output, format="PNG", optimize=True)
    return output.getvalue()


def compact_docx(path: Path = DEFAULT_DOCX, colors: int = 256) -> tuple[int, int]:
    """Rewrite the DOCX with compacted PNG media. Returns (before, after) bytes."""
    path = Path(path)
    before = path.stat().st_size
    temporary = path.with_name(path.name + ".compact.tmp")

    with zipfile.ZipFile(path, "r") as source, zipfile.ZipFile(
        temporary, "w", compression=zipfile.ZIP_DEFLATED
    ) as target:
        for item in source.infolist():
            payload = source.read(item.filename)
            if item.filename.startswith("word/media/") and item.filename.lower().endswith(".png"):
                try:
                    candidate = compact_png(payload, colors=colors)
                    if len(candidate) < len(payload):
                        payload = candidate
                except Exception:
                    # Leave any image that cannot be re-encoded untouched.
                    pass
            target.writestr(item, payload)

    temporary.replace(path)
    after = path.stat().st_size
    return before, after


def main() -> None:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DOCX
    colors = int(sys.argv[2]) if len(sys.argv) > 2 else 256
    before, after = compact_docx(target, colors=colors)
    print(
        f"Compacted {target.name}: {before:,} -> {after:,} bytes "
        f"({after / 1024 / 1024:.2f} MB)"
    )


if __name__ == "__main__":
    main()