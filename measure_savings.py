"""Measure black-outline area for representative Spanish legal and academic text.

The result is a reproducible relative coverage measurement.  It measures filled
glyph contours, including counters and composite glyphs, rather than guessing
from an arbitrary page-coverage percentage.  Physical ink mass still depends
on printer, rasterizer, paper and print profile.
"""
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).parent / "_deps"))
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.areaPen import AreaPen

ROOT = Path(__file__).parent

SAMPLES = {
    "legal": (
        "Por medio del presente instrumento, las partes declaran que han leído, "
        "comprendido y aceptado las obligaciones, plazos y condiciones establecidas. "
        "Toda modificación deberá constar por escrito y será válida desde su firma. "
        "El incumplimiento dará lugar a las acciones previstas por la normativa vigente."
    ),
    "academico": (
        "Esta investigación analiza la relación entre acceso a la información, "
        "aprendizaje y participación. Los resultados se interpretan mediante una "
        "metodología reproducible, con referencias, tablas y conclusiones verificables. "
        "La discusión reconoce límites, evidencia disponible y líneas futuras de estudio."
    ),
}

FAMILIES = {
    "legal": {
        "base_source": ROOT / "SourceSerif4-Variable.ttf",
        "outputs": [
            ("Base", ROOT / "dist/ECO-Tempura-Serif-Regular.ttf"),
            ("Plus", ROOT / "dist/ECO-Tempura-Serif-Plus-Regular.ttf"),
            ("Max", ROOT / "dist/ECO-Tempura-Serif-Max-Regular.ttf"),
        ],
    },
    "academico": {
        "base_source": Path(r"C:\Windows\Fonts\LatoWeb-Regular.ttf"),
        "outputs": [
            ("Base", ROOT / "dist/ECO-Karubi-Sans-Regular.ttf"),
            ("Plus", ROOT / "dist/ECO-Karubi-Sans-Plus-Regular.ttf"),
            ("Max", ROOT / "dist/ECO-Karubi-Sans-Max-Regular.ttf"),
        ],
    },
    "arare": {
        "base_source": ROOT / "Arimo-Variable.ttf",
        "outputs": [
            ("Base", ROOT / "dist/ECO-Arare-Sans-Regular.ttf"),
            ("Plus", ROOT / "dist/ECO-Arare-Sans-Plus-Regular.ttf"),
            ("Max", ROOT / "dist/ECO-Arare-Sans-Max-Regular.ttf"),
        ],
    },
}


def open_static(path):
    font = TTFont(path)
    if "fvar" in font:
        axes = {axis.axisTag for axis in font["fvar"].axes}
        location = {"wght": 400}
        if "opsz" in axes:
            location["opsz"] = 12
        font = instantiateVariableFont(font, location, inplace=False)
    return font


def area_for_text(font, text):
    cmap = font.getBestCmap()
    glyph_set = font.getGlyphSet()
    total = 0.0
    for character in text:
        name = cmap.get(ord(character), ".notdef")
        pen = AreaPen(glyph_set)
        glyph_set[name].draw(pen)
        total += abs(pen.value)
    return total


def main():
    result = {"method": "Área de contornos rellenados; texto regular español a 11 pt; comparación relativa contra la fuente abierta base.", "families": {}}
    for key, config in FAMILIES.items():
        source_area = area_for_text(open_static(config["base_source"]), SAMPLES["legal" if key == "legal" else "academico"])
        levels = []
        for name, path in config["outputs"]:
            area = area_for_text(open_static(path), SAMPLES["legal" if key == "legal" else "academico"])
            levels.append({"level": name, "savings_percent": round((1 - area / source_area) * 100, 4), "relative_black_area_percent": round(area / source_area * 100, 4)})
        result["families"][key] = levels
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
