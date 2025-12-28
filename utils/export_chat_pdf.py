from fpdf import FPDF
from typing import List, Dict


def export_pdf(
    history: List[Dict],
    filename: str = "chat.pdf",
    font_path: str = "utils\\fonts\\DejaVuSans.ttf",
    size: int = 12
):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Add Unicode font
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=size)

    for msg in history:
        role = msg.get("role", "user").upper()
        text = msg.get("message", "")

        pdf.multi_cell(0, 8, f"{role}: {text}")
        pdf.ln(2)

    pdf.output(filename)

def export_text(history: List[Dict], filename: str = "chat.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for msg in history:
            role = msg.get("role", "unknown")
            message = msg.get("message", "")
            f.write(f"{role}: {message}\n")
