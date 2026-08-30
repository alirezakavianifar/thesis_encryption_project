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
    
    lang = rPr.find(qn('w:lang'))
    if lang is None:
        lang = create_element('w:lang')
        rPr.append(lang)
    lang.set(qn('w:bidi'), 'fa-IR')

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
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Body Text Style
    try:
        bt = styles['Body Text']
    except KeyError:
        try:
            bt = styles['BodyText']
        except KeyError:
            bt = styles.add_style('Body Text', WD_STYLE_TYPE.PARAGRAPH)
    set_style_font(bt, name_latin=CFG.font_family_latin, name_cs=CFG.font_family_persian, size_pt=12.5)
    set_p_rtl(bt)
    bt.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    bt.paragraph_format.line_spacing = 1.35
    bt.paragraph_format.space_after = Pt(4)
    bt.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Heading 1 (Chapter Title)
    h1 = styles['Heading 1']
    set_style_font(h1, name_latin=CFG.font_family_latin, name_cs=CFG.font_family_persian, size_pt=18, bold=True, color_rgb=RGBColor(0, 0, 0))
    set_p_rtl(h1)
    h1.paragraph_format.space_before = Pt(18)
    h1.paragraph_format.space_after = Pt(12)
    h1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # Heading 2 (Section Title)
    h2 = styles['Heading 2']
    set_style_font(h2, name_latin=CFG.font_family_latin, name_cs=CFG.font_family_persian, size_pt=15, bold=True, color_rgb=RGBColor(0, 0, 0))
    set_p_rtl(h2)
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(8)
    h2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # Heading 3 (Subsection Title)
    h3 = styles['Heading 3']
    set_style_font(h3, name_latin=CFG.font_family_latin, name_cs=CFG.font_family_persian, size_pt=13.5, bold=True, color_rgb=RGBColor(0, 0, 0))
    set_p_rtl(h3)
    h3.paragraph_format.space_before = Pt(10)
    h3.paragraph_format.space_after = Pt(6)
    h3.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # Heading 4 (Sub-subsection Title)
    if 'Heading 4' in styles:
        h4 = styles['Heading 4']
    else:
        h4 = styles.add_style('Heading 4', WD_STYLE_TYPE.PARAGRAPH)
    set_style_font(h4, name_latin=CFG.font_family_latin, name_cs=CFG.font_family_persian, size_pt=12.5, bold=True, color_rgb=RGBColor(0, 0, 0))
    set_p_rtl(h4)
    h4.font.italic = False
    h4.paragraph_format.space_before = Pt(8)
    h4.paragraph_format.space_after = Pt(4)
    h4.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT

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

    # Footnote Reference character style
    try:
        fn_ref = styles['Footnote Reference']
    except KeyError:
        try:
            fn_ref = styles['FootnoteReference']
        except KeyError:
            fn_ref = styles.add_style('Footnote Reference', WD_STYLE_TYPE.CHARACTER)
    fn_ref_rPr = fn_ref._element.get_or_add_rPr()
    vertAlign = fn_ref_rPr.find(qn('w:vertAlign'))
    if vertAlign is None:
        vertAlign = create_element('w:vertAlign')
        fn_ref_rPr.append(vertAlign)
    vertAlign.set(qn('w:val'), 'superscript')
    rFonts = fn_ref_rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = create_element('w:rFonts')
        fn_ref_rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), CFG.font_family_latin)
    rFonts.set(qn('w:hAnsi'), CFG.font_family_latin)
    rFonts.set(qn('w:cs'), CFG.font_family_persian)

    # Footnote Text paragraph style
    try:
        fn_text = styles['Footnote Text']
    except KeyError:
        try:
            fn_text = styles['FootnoteText']
        except KeyError:
            fn_text = styles.add_style('Footnote Text', WD_STYLE_TYPE.PARAGRAPH)
    set_style_font(fn_text, name_latin=CFG.font_family_latin, name_cs=CFG.font_family_persian, size_pt=10)
    set_p_rtl(fn_text)
    fn_text.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    fn_text.paragraph_format.line_spacing = 1.15
    fn_text.paragraph_format.space_after = Pt(2)
    fn_text.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # SourceCode style for listings/verbatim Python code
    try:
        sc = styles['SourceCode']
    except KeyError:
        sc = styles.add_style('SourceCode', WD_STYLE_TYPE.PARAGRAPH)
    sc.font.name = "Consolas"
    sc.font.size = Pt(8.5)
    sc.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    sc.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    sc.paragraph_format.space_before = Pt(0)
    sc.paragraph_format.space_after = Pt(1)
    sc_pPr = sc._element.get_or_add_pPr()
    sc_bidi = sc_pPr.find(qn('w:bidi'))
    if sc_bidi is None:
        sc_bidi = create_element('w:bidi')
        sc_pPr.append(sc_bidi)
    sc_bidi.set(qn('w:val'), '0')
    sc_rPr = sc._element.get_or_add_rPr()
    sc_rtl = sc_rPr.find(qn('w:rtl'))
    if sc_rtl is None:
        sc_rtl = create_element('w:rtl')
        sc_rPr.append(sc_rtl)
    sc_rtl.set(qn('w:val'), '0')
    sc_rFonts = sc_rPr.find(qn('w:rFonts'))
    if sc_rFonts is None:
        sc_rFonts = create_element('w:rFonts')
        sc_rPr.append(sc_rFonts)
    sc_rFonts.set(qn('w:ascii'), 'Consolas')
    sc_rFonts.set(qn('w:hAnsi'), 'Consolas')
    sc_rFonts.set(qn('w:cs'), 'Consolas')

    doc.save(CFG.reference_docx)
    print(f"wrote {CFG.reference_docx}")

if __name__ == "__main__":
    make_reference()
