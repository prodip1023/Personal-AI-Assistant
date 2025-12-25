from fpdf import FPDF
from typing import List, Dict


def export_pdf(
    history: List[Dict],
    filename: str = "chat.pdf",
    font: str = "Helvetica",
    size: int = 13
):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font(font, size=size)

    for msg in history:
        pdf.multi_cell(0, 8, f"{msg['role'].upper()}: {msg['message']}")
        pdf.ln(2)

    pdf.output(filename)

def export_text(history: List[Dict], filename: str = "chat.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for msg in history:
            role = msg.get("role", "unknown")
            message = msg.get("message", "")
            f.write(f"{role}: {message}\n")
