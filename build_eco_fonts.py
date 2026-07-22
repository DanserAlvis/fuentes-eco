"""Build the ECO Legal and ECO Academic font families.

This is a conservative optical reduction, not a replacement for a printer's
draft mode.  Glyph advances, kerning and line metrics remain untouched; only
the filled outlines are contracted by a fixed 1.2 percent about their optical
origin.  The resulting theoretical black-area reduction is 1 - .988**2 =
2.39 percent.  At 10--12 pt this is below normal office-printer dot gain,
which makes it a safe starting point for contracts, theses and forms.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "_deps"))

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.ttLib.tables.ttProgram import Program

ROOT = Path(__file__).parent
OUT = ROOT / "dist"
LEVELS = {
    # scale, file suffix, family-name suffix
    "Base": (0.988, "", ""),
    "Plus": (0.975, "-Plus", " Plus"),
    "Max": (0.960, "-Max", " Max"),
}


def set_name(font, name_id, value):
    """Set Windows Unicode and Macintosh English name records."""
    names = font["name"]
    for record in names.names:
        if record.nameID == name_id and record.platformID in (1, 3):
            record.string = value.encode("utf-16-be" if record.platformID == 3 else "mac_roman", "replace")
    if not any(r.nameID == name_id for r in names.names):
        names.setName(value, name_id, 3, 1, 0x0409)
        names.setName(value, name_id, 1, 0, 0)


def contract_outlines(font, scale):
    glyf = font["glyf"]
    empty = Program()
    # Simple glyphs are contracted around the advance-width centre and baseline.
    # Keeping the advance width constant prevents reflow in existing documents.
    for glyph_name in font.getGlyphOrder():
        glyph = glyf[glyph_name]
        if glyph.isComposite() or not glyph.numberOfContours:
            continue
        glyph.expand(glyf)
        if not hasattr(glyph, "coordinates"):
            continue
        advance = font["hmtx"].metrics[glyph_name][0]
        centre = advance / 2
        for index, point in enumerate(glyph.coordinates):
            glyph.coordinates[index] = (
                round(centre + (point[0] - centre) * scale),
                round(point[1] * scale),
            )
        glyph.program = empty
    # Composite glyphs inherit contracted components.  Their placement is left
    # unchanged so accented characters retain robust mark attachment.
    for glyph_name in font.getGlyphOrder():
        glyph = glyf[glyph_name]
        if glyph.isComposite():
            glyph.program = empty
    for tag in ("cvt ", "fpgm", "prep"):
        if tag in font:
            del font[tag]


def build(source, output_name, family, style, weight=None, scale=0.988):
    font = TTFont(str(source), recalcBBoxes=True, recalcTimestamp=False)
    if "fvar" in font:
        available_axes = {axis.axisTag for axis in font["fvar"].axes}
        location = {"wght": weight}
        if "opsz" in available_axes:
            location["opsz"] = 12
        font = instantiateVariableFont(font, location, inplace=False, optimize=True)
    contract_outlines(font, scale)
    full_name = f"{family} {style}"
    set_name(font, 1, family)
    set_name(font, 2, style)
    set_name(font, 3, f"ECO; {family}-{style.replace(' ', '')}; 1.000")
    set_name(font, 4, full_name)
    set_name(font, 6, f"{family.replace(' ', '')}-{style.replace(' ', '')}")
    set_name(font, 16, family)
    set_name(font, 17, style)
    font["head"].fontRevision = 1.0
    font["OS/2"].usWeightClass = 700 if "Bold" in style else 400
    OUT.mkdir(exist_ok=True)
    font.save(str(OUT / output_name))


def main():
    sources = [
        (ROOT / "SourceSerif4-Variable.ttf", "ECO-Legal-Serif", "ECO Legal Serif", "Regular", 400),
        (ROOT / "SourceSerif4-Variable.ttf", "ECO-Legal-Serif", "ECO Legal Serif", "Bold", 700),
        (ROOT / "SourceSerif4-Italic-Variable.ttf", "ECO-Legal-Serif", "ECO Legal Serif", "Italic", 400),
        (ROOT / "SourceSerif4-Italic-Variable.ttf", "ECO-Legal-Serif", "ECO Legal Serif", "Bold Italic", 700),
        (Path(r"C:\Windows\Fonts\LatoWeb-Regular.ttf"), "ECO-Academic-Sans", "ECO Academic Sans", "Regular", None),
        (Path(r"C:\Windows\Fonts\LatoWeb-Bold.ttf"), "ECO-Academic-Sans", "ECO Academic Sans", "Bold", None),
        (Path(r"C:\Windows\Fonts\LatoWeb-Italic.ttf"), "ECO-Academic-Sans", "ECO Academic Sans", "Italic", None),
        (Path(r"C:\Windows\Fonts\LatoWeb-BoldItalic.ttf"), "ECO-Academic-Sans", "ECO Academic Sans", "Bold Italic", None),
        (ROOT / "Arimo-Variable.ttf", "ECO-Arial-Compatible-Sans", "ECO Arial Compatible Sans", "Regular", 400),
        (ROOT / "Arimo-Variable.ttf", "ECO-Arial-Compatible-Sans", "ECO Arial Compatible Sans", "Bold", 700),
        (ROOT / "Arimo-Italic-Variable.ttf", "ECO-Arial-Compatible-Sans", "ECO Arial Compatible Sans", "Italic", 400),
        (ROOT / "Arimo-Italic-Variable.ttf", "ECO-Arial-Compatible-Sans", "ECO Arial Compatible Sans", "Bold Italic", 700),
    ]
    for level, (scale, file_suffix, family_suffix) in LEVELS.items():
        for source, file_prefix, family, style, weight in sources:
            output_name = f"{file_prefix}{file_suffix}-{style.replace(' ', '')}.ttf"
            build(source, output_name, family + family_suffix, style, weight, scale)
            print(f"built {output_name}")


if __name__ == "__main__":
    main()
