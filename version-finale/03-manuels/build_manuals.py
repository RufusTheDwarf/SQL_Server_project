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

def set_black(run, name="Arial", size=10, bold=None):
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


def set_paragraph_border(paragraph, edge="bottom", size="5", space="3"):
    ppr = paragraph._p.get_or_add_pPr()
    borders = ppr.find(qn("w:pBdr"))
    if borders is None:
        borders = OxmlElement("w:pBdr")
        ppr.append(borders)
    border = borders.find(qn("w:" + edge))
    if border is None:
        border = OxmlElement("w:" + edge)
        borders.append(border)
    border.set(qn("w:val"), "single")
    border.set(qn("w:sz"), size)
    border.set(qn("w:space"), space)
    border.set(qn("w:color"), "000000")


def set_paragraph_shading(paragraph):
    ppr = paragraph._p.get_or_add_pPr()
    shading = ppr.find(qn("w:shd"))
    if shading is None:
        shading = OxmlElement("w:shd")
        ppr.append(shading)
    shading.set(qn("w:val"), "clear")
    shading.set(qn("w:fill"), "F4F4F4")


def polish_document(doc):
    # Neutralise every Word theme style, including the unused Title/Subtitle defaults.
    for style in doc.styles:
        try:
            style.font.color.rgb = BLACK
            color = style._element.get_or_add_rPr().find(qn("w:color"))
            if color is not None:
                color.set(qn("w:val"), "000000")
                for attr in (qn("w:themeColor"), qn("w:themeTint"), qn("w:themeShade")):
                    color.attrib.pop(attr, None)
        except (AttributeError, TypeError):
            pass

    for name, size, bold, italic in (
        ("Normal", 10.1, False, False),
        ("Title", 23, True, False),
        ("Subtitle", 10.8, True, False),
        ("Heading 1", 13.2, True, False),
        ("Heading 2", 10.9, True, False),
        ("Heading 3", 10.2, True, True),
    ):
        style = doc.styles[name]
        style.font.name = "Arial"
        style.font.size = Pt(size)
        style.font.bold = bold
        style.font.italic = italic
        style.font.color.rgb = BLACK
        rpr = style._element.get_or_add_rPr()
        color = rpr.find(qn("w:color"))
        if color is None:
            color = OxmlElement("w:color")
            rpr.append(color)
        color.set(qn("w:val"), "000000")
        for attr in (qn("w:themeColor"), qn("w:themeTint"), qn("w:themeShade")):
            color.attrib.pop(attr, None)

    section = doc.sections[0]
    section.page_width, section.page_height = Cm(21), Cm(29.7)
    section.top_margin, section.bottom_margin = Cm(1.65), Cm(1.5)
    section.left_margin, section.right_margin = Cm(2), Cm(2)
    section.header_distance, section.footer_distance = Cm(0.75), Cm(0.75)

    header = section.header.paragraphs[0]
    header.clear()
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = header.add_run("ETML  |  JOURNÉES PORTES OUVERTES")
    set_black(run, "Arial", 7.5, True)
    header.paragraph_format.space_after = Pt(2)
    set_paragraph_border(header, "bottom", "4", "4")

    footer = section.footer.paragraphs[0]
    footer.clear()
    add_page_number(footer)

    paragraphs = [p for p in doc.paragraphs if p.text.strip()]
    title_block = []
    if paragraphs:
        title = paragraphs[0]
        title.style = doc.styles["Title"]
        title.alignment = WD_ALIGN_PARAGRAPH.LEFT
        title.paragraph_format.space_before = Pt(8)
        title.paragraph_format.space_after = Pt(3)
        title.paragraph_format.keep_with_next = True
        for run in title.runs:
            set_black(run, "Arial", 23, True)
        set_paragraph_border(title, "bottom", "8", "6")

        # Only paragraphs before the first section heading belong to the title block.
        for candidate in paragraphs[1:]:
            if candidate.style.name.startswith("Heading"):
                break
            title_block.append(candidate)

        if len(title_block) >= 3:
            subtitle, institution, version = title_block[:3]
            subtitle.style = doc.styles["Subtitle"]
            subtitle.paragraph_format.space_after = Pt(1)
            subtitle.paragraph_format.keep_with_next = True
            for run in subtitle.runs:
                set_black(run, "Arial", 10.8, True)
            institution.paragraph_format.space_after = Pt(1)
            institution.paragraph_format.keep_with_next = True
            for run in institution.runs:
                set_black(run, "Arial", 8.3, True)
            version.paragraph_format.space_after = Pt(8)
            version.paragraph_format.keep_with_next = True
            for run in version.runs:
                set_black(run, "Arial", 8.2)
                run.italic = True
        elif len(title_block) == 1:
            institution = title_block[0]
            institution.paragraph_format.space_after = Pt(7)
            institution.paragraph_format.keep_with_next = True
            for run in institution.runs:
                set_black(run, "Arial", 8.3, True)

    for paragraph in doc.paragraphs:
        value = paragraph.text.strip()
        if not value or paragraph is paragraphs[0] or paragraph in title_block:
            continue
        if paragraph.style.name == "Heading 1":
            paragraph.paragraph_format.space_before = Pt(9)
            paragraph.paragraph_format.space_after = Pt(3)
            paragraph.paragraph_format.keep_with_next = True
            paragraph.paragraph_format.keep_together = True
            for run in paragraph.runs:
                set_black(run, "Arial", 13.2, True)
            set_paragraph_border(paragraph, "bottom", "5", "3")
        elif paragraph.style.name == "Heading 2":
            paragraph.paragraph_format.space_before = Pt(5.5)
            paragraph.paragraph_format.space_after = Pt(2)
            paragraph.paragraph_format.keep_with_next = True
            paragraph.paragraph_format.keep_together = True
            for run in paragraph.runs:
                set_black(run, "Arial", 10.9, True)
        elif paragraph.style.name == "Heading 3":
            paragraph.paragraph_format.space_before = Pt(4)
            paragraph.paragraph_format.space_after = Pt(1.5)
            paragraph.paragraph_format.keep_with_next = True
            for run in paragraph.runs:
                set_black(run, "Arial", 10.2, True)
                run.italic = True
        else:
            paragraph.paragraph_format.line_spacing = 1.08
            paragraph.paragraph_format.space_after = Pt(4.3)
            paragraph.paragraph_format.keep_together = True
            # A code block is a single Consolas run at 8 pt; inline code remains inline.
            code_block = (
                len(paragraph.runs) == 1
                and paragraph.runs[0].font.name == "Consolas"
                and paragraph.runs[0].font.size is not None
                and paragraph.runs[0].font.size.pt <= 8
            )
            if code_block:
                paragraph.paragraph_format.left_indent = Cm(0.35)
                paragraph.paragraph_format.right_indent = Cm(0.15)
                paragraph.paragraph_format.space_before = Pt(3)
                paragraph.paragraph_format.space_after = Pt(6)
                paragraph.paragraph_format.line_spacing = 1.0
                set_paragraph_shading(paragraph)
                set_paragraph_border(paragraph, "left", "10", "5")
                set_black(paragraph.runs[0], "Consolas", 8.1)
            else:
                if value.startswith("- "):
                    paragraph.paragraph_format.left_indent = Cm(0.55)
                    paragraph.paragraph_format.first_line_indent = Cm(-0.35)
                    paragraph.paragraph_format.space_after = Pt(2)
                elif re.match(r"^\d+\.\s+", value):
                    paragraph.paragraph_format.left_indent = Cm(0.55)
                    paragraph.paragraph_format.first_line_indent = Cm(-0.45)
                    paragraph.paragraph_format.space_after = Pt(2.5)
                for run in paragraph.runs:
                    if run.font.name == "Consolas":
                        set_black(run, "Consolas", 9)
                    else:
                        set_black(run, "Arial", 10.1, run.bold)
                        run.italic = run.italic

    # Explicit black run colors prevent Word/LibreOffice theme overrides.
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            run.font.color.rgb = BLACK
            color = run._element.get_or_add_rPr().find(qn("w:color"))
            if color is not None:
                color.set(qn("w:val"), "000000")
                for attr in (qn("w:themeColor"), qn("w:themeTint"), qn("w:themeShade")):
                    color.attrib.pop(attr, None)


def make_docx(source_path, output_path):
    text = source_path.read_text(encoding="utf-8")
    if chr(0x2013) in text or chr(0x2014) in text:
        raise ValueError("Ponctuation longue interdite dans " + source_path.name)
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.top_margin, sec.bottom_margin = Cm(1.5), Cm(1.4)
    sec.left_margin, sec.right_margin = Cm(2.0), Cm(2.0)

    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(10)
    normal.font.color.rgb = BLACK
    normal.paragraph_format.space_after = Pt(3)
    normal.paragraph_format.line_spacing = 1.0

    for name, size in (("Heading 1", 14.5), ("Heading 2", 11.5), ("Heading 3", 10.5)):
        style = doc.styles[name]
        style.font.name = "Arial"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = BLACK
        style.paragraph_format.space_before = Pt(7 if name == "Heading 1" else 5)
        style.paragraph_format.space_after = Pt(2.5)
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
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(4)
                p.paragraph_format.keep_together = True
                run = p.add_run(chr(10).join(code_lines))
                set_black(run, "Consolas", 8)
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
            p.paragraph_format.space_after = Pt(1.5)
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
    polish_document(doc)
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
