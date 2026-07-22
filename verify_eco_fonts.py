"""Minimal integrity and metadata check for the generated ECO font files."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "_deps"))
from fontTools.ttLib import TTFont

for path in sorted((Path(__file__).parent / "dist").glob("*.ttf")):
    font = TTFont(path)
    print(f"{path.name}: {font['name'].getDebugName(1)} | variable={'fvar' in font} | glyphs={font['maxp'].numGlyphs}")
