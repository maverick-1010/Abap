"""Paths and font registration shared by all scripts."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
DATA = ROOT / "data"
OUT = ROOT / "out"
sys.path.insert(0, str(SRC / "vendor"))   # locally installed iapws
sys.path.insert(0, str(SRC))

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def register_fonts():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.fonts import addMapping
    pdfmetrics.registerFont(TTFont("DV", str(FONT_DIR / "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("DV-B", str(FONT_DIR / "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("DVM", str(FONT_DIR / "DejaVuSansMono.ttf")))
    pdfmetrics.registerFont(TTFont("DVM-B", str(FONT_DIR / "DejaVuSansMono-Bold.ttf")))
    addMapping("DV", 0, 0, "DV")
    addMapping("DV", 1, 0, "DV-B")
    addMapping("DV", 0, 1, "DV")
    addMapping("DV", 1, 1, "DV-B")
