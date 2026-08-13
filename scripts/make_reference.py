import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from projectcfg import CFG

def create_element(name):
    return OxmlElement(name)

def set_font(run, name_latin="Calibri", name_cs="B Lotus"):
    rPr = run._r.get_or_add_rPr()
    rFonts = create_element('w:rFonts')
    rFonts.set(qn('w:ascii'), name_latin)
    rFonts.set(qn('w:hAnsi'), name_latin)
    rFonts.set(qn('w:cs'), name_cs)
    rPr.append(rFonts)

def set_style_font(style, name_latin="Calibri", name_cs="B Lotus", size_pt=12, bold=False, color_rgb=None):
    style.font.name = name_latin
    style.font.size = Pt(size_pt)
    style.font.bold = bold
    if color_rgb:
        style.font.color.rgb = color_rgb
    
    rPr = style._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = create_element('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), name_latin)
    rFonts.set(qn('w:hAnsi'), name_latin)
    rFonts.set(qn('w:cs'), name_cs)

def set_p_rtl(style):
    pPr = style._element.get_or_add_pPr()
    bidi = pPr.find(qn('w:bidi'))
    if bidi is None:
        bidi = create_element('w:bidi')
        pPr.append(bidi)
    bidi.set(qn('w:val'), '1')

    rPr = style._element.get_or_add_rPr()
    rtl = rPr.find(qn('w:rtl'))
    if rtl is None:
        rtl = create_element('w:rtl')
        rPr.append(rtl)
    rtl.set(qn('w:val'), '1')

def make_reference():
    doc = Document()
    
    # Configure sections & page margins (3cm Right for binding, 2.5cm Left, Top, Bottom)
    for section in doc.sections:
        section.top_margin = Inches(0.98)     # 2.5 cm
        section.bottom_margin = Inches(0.98)  # 2.5 cm
        section.right_margin = Inches(1.18)   # 3.0 cm (binding margin)
        section.left_margin = Inches(0.98)    # 2.5 cm

    styles = doc.styles

    # Normal Style (Body Text)
    normal = styles['Normal']
    set_style_font(normal, name_latin=CFG.font_family_latin, name_cs=CFG.font_family_persian, size_pt=12.5)
    set_p_rtl(normal)
    normal.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    normal.paragraph_format.line_spacing = 1.35
    normal.paragraph_format.space_after = Pt(4)
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # Heading 1 (Chapter Title)
    h1 = styles['Heading 1']
    set_style_font(h1, name_latin=CFG.font_family_latin, name_cs=CFG.font_family_persian, size_pt=18, bold=True, color_rgb=RGBColor(0, 51, 102))
    set_p_rtl(h1)
    h1.paragraph_format.space_before = Pt(18)
    h1.paragraph_format.space_after = Pt(12)
    h1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # Heading 2 (Section Title)
    h2 = styles['Heading 2']
    set_style_font(h2, name_latin=CFG.font_family_latin, name_cs=CFG.font_family_persian, size_pt=15, bold=True, color_rgb=RGBColor(0, 70, 130))
    set_p_rtl(h2)
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(8)
    h2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # Heading 3 (Subsection Title)
    h3 = styles['Heading 3']
    set_style_font(h3, name_latin=CFG.font_family_latin, name_cs=CFG.font_family_persian, size_pt=13.5, bold=True, color_rgb=RGBColor(50, 50, 50))
    set_p_rtl(h3)
    h3.paragraph_format.space_before = Pt(10)
    h3.paragraph_format.space_after = Pt(6)
    h3.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # Caption Style (generic base)
    if 'Caption' in styles:
        cap = styles['Caption']
    else:
        cap = styles.add_style('Caption', WD_STYLE_TYPE.PARAGRAPH)
    set_style_font(cap, name_latin=CFG.font_family_latin, name_cs=CFG.font_family_persian, size_pt=10.5, bold=True, color_rgb=RGBColor(60, 60, 60))
    set_p_rtl(cap)
    cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(6)
    cap.paragraph_format.space_after = Pt(6)

    # CaptionTable style - used by TOC \t "CaptionTable,1" to generate List of Tables
    if 'CaptionTable' in styles:
        ctab = styles['CaptionTable']
    else:
        ctab = styles.add_style('CaptionTable', WD_STYLE_TYPE.PARAGRAPH)
    set_style_font(ctab, name_latin=CFG.font_family_latin, name_cs=CFG.font_family_persian, size_pt=10.5, bold=True, color_rgb=RGBColor(60, 60, 60))
    set_p_rtl(ctab)
    ctab.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ctab.paragraph_format.space_before = Pt(4)
    ctab.paragraph_format.space_after = Pt(4)

    # CaptionFigure style - used by TOC \t "CaptionFigure,1" to generate List of Figures
    if 'CaptionFigure' in styles:
        cfig = styles['CaptionFigure']
    else:
        cfig = styles.add_style('CaptionFigure', WD_STYLE_TYPE.PARAGRAPH)
    set_style_font(cfig, name_latin=CFG.font_family_latin, name_cs=CFG.font_family_persian, size_pt=10.5, bold=True, color_rgb=RGBColor(60, 60, 60))
    set_p_rtl(cfig)
    cfig.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cfig.paragraph_format.space_before = Pt(4)
    cfig.paragraph_format.space_after = Pt(4)

    doc.save(CFG.reference_docx)
    print(f"wrote {CFG.reference_docx}")

if __name__ == "__main__":
    make_reference()
