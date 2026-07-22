"""Create redistributable ZIP packages with the required OFL notices."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
RELEASES = ROOT / "releases"

FAMILIES = {
    "ECO-Tempura-Serif": "NOTICE-Source-Serif-4.txt",
    "ECO-Karubi-Sans": "NOTICE-Lato.txt",
    "ECO-Arare-Sans": "NOTICE-Arimo.txt",
}
LEVELS = ("Base", "Plus", "Max")
STYLES = ("Regular", "Italic", "Bold", "BoldItalic")


def filename(prefix, level, style):
    suffix = "" if level == "Base" else f"-{level}"
    return f"{prefix}{suffix}-{style}.ttf"


def main():
    RELEASES.mkdir(exist_ok=True)
    for prefix, notice in FAMILIES.items():
        for level in LEVELS:
            archive = RELEASES / f"{prefix}-{level}.zip"
            with ZipFile(archive, "w", ZIP_DEFLATED) as zip_file:
                for style in STYLES:
                    path = DIST / filename(prefix, level, style)
                    zip_file.write(path, path.name)
                zip_file.write(ROOT / "LICENSES" / "OFL-1.1.txt", "OFL-1.1.txt")
                zip_file.write(ROOT / "LICENSES" / notice, notice)
            print(f"built {archive.name}")


if __name__ == "__main__":
    main()
