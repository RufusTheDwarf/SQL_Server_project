from __future__ import annotations
import re, shutil, subprocess
from pathlib import Path
from zipfile import ZipFile
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source"
MANUALS = [
    ("01-manuel-installation.md", "L-141-Rafael_Melo-ManuelInstallation"),
    ("02-manuel-animation.md", "D-141-Rafael_Melo-ManuelAnimateur"),
    ("03-fiche-visiteur.md", "D-141-Rafael_Melo-ManuelVisiteur"),
]
BLACK = RGBColor(0, 0, 0)
TICK = chr(96)

def set_black(run, name="Arial", size=10.5, bold=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.color.rgb = BLACK
    if bold is not None:
        run.bold = bold

def add_inline(paragraph, value):
    pattern = "(" + TICK + "[^" + TICK + "]+" + TICK + r"|\*\*.*?\*\*)"
    for piece in re.split(pattern, value):
        if not piece:
            continue
        if piece.startswith(TICK) and piece.endswith(TICK):
            run = paragraph.add_run(piece[1:-1])
            set_black(run, "Consolas", 9)
        elif piece.startswith("**") and piece.endswith("**"):
            run = paragraph.add_run(piece[2:-2])
            set_black(run, "Arial", 10.5, True)
        else:
            run = paragraph.add_run(piece)
            set_black(run)

def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run("Mission SQL Cinéma - ETML  |  ")
    set_black(run, "Arial", 8)
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    paragraph._p.append(field)

def make_docx(source_path, output_path):
    text = source_path.read_text(encoding="utf-8")
    if chr(0x2013) in text or chr(0x2014) in text:
        raise ValueError("Ponctuation longue interdite dans " + source_path.name)
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.top_margin, sec.bottom_margin = Cm(1.75), Cm(1.65)
    sec.left_margin, sec.right_margin = Cm(2.0), Cm(2.0)

    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = BLACK
    normal.paragraph_format.space_after = Pt(4)
    normal.paragraph_format.line_spacing = 1.05

    for name, size in (("Heading 1", 15), ("Heading 2", 12.5), ("Heading 3", 11)):
        style = doc.styles[name]
        style.font.name = "Arial"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = BLACK
        style.paragraph_format.space_before = Pt(10 if name == "Heading 1" else 7)
        style.paragraph_format.space_after = Pt(3)
        style.paragraph_format.keep_with_next = True
        style.paragraph_format.keep_together = True

    header = sec.header.paragraphs[0]
    header.text = "ETML - JOURNÉES PORTES OUVERTES"
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for run in header.runs:
        set_black(run, "Arial", 8)
    add_page_number(sec.footer.paragraphs[0])

    in_code, code_lines = False, []
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith(TICK * 3):
            if not in_code:
                in_code, code_lines = True, []
            else:
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Cm(0.55)
                p.paragraph_format.right_indent = Cm(0.25)
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(6)
                p.paragraph_format.keep_together = True
                run = p.add_run(chr(10).join(code_lines))
                set_black(run, "Consolas", 8.5)
                in_code = False
            continue
        if in_code:
            code_lines.append(raw.rstrip())
            continue
        if not line:
            continue
        if line.startswith("# "):
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(5)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(line[2:])
            set_black(run, "Arial", 21, True)
        elif line.startswith("## "):
            p = doc.add_paragraph(style="Heading 1")
            p.add_run(line[3:])
        elif line.startswith("### "):
            p = doc.add_paragraph(style="Heading 2")
            p.add_run(line[4:])
        elif line.startswith("- "):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.45)
            p.paragraph_format.first_line_indent = Cm(-0.35)
            p.paragraph_format.space_after = Pt(2)
            add_inline(p, "- " + line[2:])
        else:
            number = re.match(r"^(\d+)\.\s+(.*)$", line)
            p = doc.add_paragraph()
            p.paragraph_format.keep_together = True
            if number:
                p.paragraph_format.left_indent = Cm(0.55)
                p.paragraph_format.first_line_indent = Cm(-0.45)
                p.paragraph_format.space_after = Pt(2)
                add_inline(p, number.group(1) + ". " + number.group(2))
            else:
                add_inline(p, line)

    if in_code:
        raise ValueError("Bloc de code non referme dans " + source_path.name)
    doc.core_properties.title = output_path.stem.replace("_", " ")
    doc.core_properties.subject = "Mission SQL Cinema - ETML"
    doc.core_properties.author = ""
    doc.core_properties.last_modified_by = ""
    doc.core_properties.comments = ""
    doc.core_properties.keywords = ""
    doc.save(output_path)

    reopened = Document(output_path)
    if not reopened.paragraphs or reopened.tables:
        raise RuntimeError("Structure DOCX invalide : " + output_path.name)
    with ZipFile(output_path) as archive:
        if archive.testzip() is not None:
            raise RuntimeError("Archive DOCX endommagee : " + output_path.name)

def main():
    for source_name, output_stem in MANUALS:
        make_docx(SOURCE / source_name, ROOT / (output_stem + ".docx"))
    office = shutil.which("libreoffice") or shutil.which("soffice")
    if not office:
        raise RuntimeError("LibreOffice est requis pour produire les PDF.")
    for _, output_stem in MANUALS:
        docx_path = ROOT / (output_stem + ".docx")
        result = subprocess.run(
            [office, "--headless", "--convert-to", "pdf", "--outdir", str(ROOT), str(docx_path)],
            capture_output=True, text=True
        )
        pdf_path = ROOT / (output_stem + ".pdf")
        if result.returncode != 0 or not pdf_path.exists() or pdf_path.stat().st_size == 0:
            raise RuntimeError("Conversion PDF echouee : " + output_stem + "\n" + result.stderr)
    for _, output_stem in MANUALS:
        docx_path = ROOT / (output_stem + ".docx")
        pdf_path = ROOT / (output_stem + ".pdf")
        Document(docx_path)
        if docx_path.stat().st_size < 5000 or pdf_path.stat().st_size < 1000:
            raise RuntimeError("Fichier final anormalement petit : " + output_stem)
    print("Trois manuels Word et PDF generes et verifies.")

if __name__ == "__main__":
    main()
