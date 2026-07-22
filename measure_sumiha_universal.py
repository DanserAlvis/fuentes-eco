"""Measure rasterized coverage of ECO Sumiha Beta against Arimo Regular.

Both fonts render the same text at 11 pt and 600 dpi. Grayscale pixel coverage
is summed, so overlapping contours count only once, as they do in normal
browser/printer rasterization. This remains a simulation, not physical ink use.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
DPI = 600
POINT_SIZE = 11
PIXEL_SIZE = round(POINT_SIZE / 72 * DPI)
TEXTS = {
    "legal": "Las partes declaran que han leído y aceptado las obligaciones, plazos y condiciones establecidas en este documento.",
    "academico": "Esta investigación presenta evidencia verificable, metodología reproducible y conclusiones para futuras líneas de estudio.",
    "oficina": "El informe administrativo resume resultados, fechas, responsables y próximos pasos de manera clara para todas las personas.",
}


def raster_coverage(font_path, text):
    font = ImageFont.truetype(str(font_path), PIXEL_SIZE)
    probe = Image.new("L", (1, 1), 255)
    probe_draw = ImageDraw.Draw(probe)
    bbox = probe_draw.textbbox((0, 0), text, font=font)
    width, height = bbox[2] - bbox[0] + 8, bbox[3] - bbox[1] + 8
    image = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(image)
    draw.text((4 - bbox[0], 4 - bbox[1]), text, font=font, fill=0)
    return sum(255 - value for value in image.get_flattened_data()) / 255


def main():
    eco_path = ROOT / "dist/ECO-Sumiha-Beta-Regular.ttf"
    reference_path = ROOT / "Arimo-Variable.ttf"
    values = []
    for label, text in TEXTS.items():
        eco = raster_coverage(eco_path, text)
        reference = raster_coverage(reference_path, text)
        reduction = (1 - eco / reference) * 100
        values.append(reduction)
        print(f"{label}: {reduction:.2f}%")
    print(f"average: {sum(values)/len(values):.2f}%")
    print(f"method: grayscale raster coverage, {POINT_SIZE} pt, {DPI} dpi")


if __name__ == "__main__":
    main()
