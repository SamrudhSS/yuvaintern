# -*- coding: utf-8 -*-
"""Shared helpers for building the Week 1 agribusiness plan."""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

PRIMARY = "1B4332"
SECONDARY = "2D6A4F"
ACCENT = "B5651D"
PALE = "EDF3EE"
PALE2 = "F7F9F6"
RULE = "C9D6CC"
INK = "1F2421"
MUTED = "5C6B62"
WHITE = "FFFFFF"
BODY = "Calibri"
CONTENT_W = 16.6

TABLE_NO = [0]
FIG_NO = [0]


def el(tag, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn(k), str(v))
    return e


def run_font(run, size=None, bold=None, italic=None, color=None, name=BODY):
    run.font.name = name
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.append(rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), name)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color is not None:
        run.font.color.rgb = RGBColor.from_string(color)


def spacing(run, twips):
    run._element.get_or_add_rPr().append(el("w:spacing", **{"w:val": twips}))


def shade(cell, hex_fill):
    tcpr = cell._tc.get_or_add_tcPr()
    for old in tcpr.findall(qn("w:shd")):
        tcpr.remove(old)
    tcpr.append(el("w:shd", **{"w:val": "clear", "w:color": "auto", "w:fill": hex_fill}))


def cell_borders(cell, color=RULE, sz=4, sides=("top", "left", "bottom", "right")):
    tcpr = cell._tc.get_or_add_tcPr()
    borders = tcpr.find(qn("w:tcBorders"))
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tcpr.append(borders)
    for s in sides:
        borders.append(el(f"w:{s}", **{"w:val": "single", "w:sz": sz, "w:space": 0, "w:color": color}))
    tcpr.append(borders)


def no_borders(table):
    tblpr = table._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for s in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b.append(el(f"w:{s}", **{"w:val": "none", "w:sz": 0, "w:space": 0, "w:color": "auto"}))
    tblpr.append(b)


def thin_borders(table, color=RULE, sz=4):
    tblpr = table._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for s in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b.append(el(f"w:{s}", **{"w:val": "single", "w:sz": sz, "w:space": 0, "w:color": color}))
    tblpr.append(b)


def cell_margins(table, top=60, bottom=60, left=90, right=90):
    tblpr = table._tbl.tblPr
    m = OxmlElement("w:tblCellMar")
    for k, v in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        m.append(el(f"w:{k}", **{"w:w": v, "w:type": "dxa"}))
    tblpr.append(m)


def fixed_layout(table, widths):
    table.autofit = False
    tblpr = table._tbl.tblPr
    tblpr.append(el("w:tblLayout", **{"w:type": "fixed"}))
    tblpr.append(el("w:tblW", **{"w:w": int(sum(widths) * 567), "w:type": "dxa"}))
    for row in table.rows:
        for i, w in enumerate(widths):
            if i < len(row.cells):
                row.cells[i].width = Cm(w)


def repeat_header(row):
    row._tr.get_or_add_trPr().append(el("w:tblHeader", **{"w:val": "true"}))


def no_split(row):
    row._tr.get_or_add_trPr().append(el("w:cantSplit", **{"w:val": "true"}))


def write_cell(cell, text, size=8.5, bold=False, color=INK, align=None, italic=False):
    cell.text = ""
    para = cell.paragraphs[0]
    para.paragraph_format.space_before = Pt(0)
    para.paragraph_format.space_after = Pt(0)
    para.paragraph_format.line_spacing = 1.05
    if align:
        para.alignment = align
    clean = str(text).replace("<br>", "\n")
    for i, line in enumerate(clean.split("\n")):
        if i:
            para.add_run().add_break()
        r = para.add_run(line)
        run_font(r, size=size, bold=bold, color=color, italic=italic)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER if bold else WD_ALIGN_VERTICAL.TOP


def caption(doc, text, label="Table"):
    if label == "Table":
        TABLE_NO[0] += 1
        number = TABLE_NO[0]
    else:
        FIG_NO[0] += 1
        number = FIG_NO[0]
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(10 if label == "Table" else 4)
    pf.space_after = Pt(4 if label == "Table" else 10)
    pf.keep_with_next = label == "Table"
    r = p.add_run(f"{label} {number}. ")
    run_font(r, size=8.5, bold=True, color=SECONDARY)
    r2 = p.add_run(text)
    run_font(r2, size=8.5, italic=True, color=MUTED)
    return p


def table(doc, headers, rows, widths, size=8.5, header_size=8.5, zebra=True,
          first_col_bold=False, align_center=None, caption_text=None, keep_together=False):
    if caption_text:
        caption(doc, caption_text)
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = 1
    thin_borders(t)
    cell_margins(t)
    hdr = t.rows[0]
    for i, h in enumerate(headers):
        c = hdr.cells[i]
        write_cell(c, h, size=header_size, bold=True, color=WHITE)
        shade(c, PRIMARY)
        c.paragraphs[0].paragraph_format.keep_with_next = True
    repeat_header(hdr)
    no_split(hdr)
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        no_split(t.rows[-1])
        for ci, val in enumerate(row):
            bold = first_col_bold and ci == 0
            write_cell(cells[ci], val, size=size, bold=bold,
                       color=PRIMARY if bold else INK)
            if zebra and ri % 2 == 1:
                shade(cells[ci], PALE2)
            if align_center and ci in align_center:
                cells[ci].paragraphs[0].alignment = 1
    fixed_layout(t, widths)
    # avoid a lone final row spilling onto the next page
    if keep_together:
        for row in t.rows[:-1]:
            for c in row.cells:
                for p in c.paragraphs:
                    p.paragraph_format.keep_with_next = True
    elif len(t.rows) > 2:
        for c in t.rows[-2].cells:
            for p in c.paragraphs:
                p.paragraph_format.keep_with_next = True
    spacer(doc, 8)
    return t


def spacer(doc, pts=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1
    r = p.add_run("")
    run_font(r, size=max(1, pts // 2))
    return p


def para(doc, text, size=10.5, space_after=7, space_before=0, italic=False,
         color=INK, align=None, keep=False, bold_lead=None):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.13
    if align:
        p.alignment = align
    if keep:
        pf.keep_with_next = True
    if bold_lead:
        r = p.add_run(bold_lead)
        run_font(r, size=size, bold=True, color=PRIMARY)
    r = p.add_run(text)
    run_font(r, size=size, italic=italic, color=color)
    return p


def bullet(doc, text, level=0, size=10.5, lead=None, space_after=3):
    p = doc.add_paragraph(style="List Bullet")
    pf = p.paragraph_format
    pf.left_indent = Cm(0.65 + 0.55 * level)
    pf.first_line_indent = Cm(-0.4)
    pf.space_before = Pt(0)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.12
    if lead:
        r = p.add_run(lead)
        run_font(r, size=size, bold=True, color=PRIMARY)
    r = p.add_run(text)
    run_font(r, size=size, color=INK)
    return p


def plain_title(doc, text, size=15, rule=True, space_before=0, space_after=8):
    """A title that looks like a heading but is not part of the heading hierarchy."""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.keep_with_next = True
    r = p.add_run(text)
    run_font(r, size=size, bold=True, color=PRIMARY)
    if rule:
        ppr = p._p.get_or_add_pPr()
        bdr = OxmlElement("w:pBdr")
        bdr.append(el("w:bottom", **{"w:val": "single", "w:sz": 10,
                                    "w:space": 6, "w:color": ACCENT}))
        ppr.append(bdr)
    return p


def h1(doc, text, page_break=False):
    p = doc.add_paragraph(style="Heading 1")
    if page_break:
        p.paragraph_format.page_break_before = True
    pf = p.paragraph_format
    pf.space_before = Pt(26)
    pf.space_after = Pt(10)
    pf.keep_with_next = True
    r = p.add_run(text)
    run_font(r, size=17, bold=True, color=PRIMARY)
    ppr = p._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    bdr.append(el("w:bottom", **{"w:val": "single", "w:sz": 10, "w:space": 6, "w:color": ACCENT}))
    ppr.append(bdr)
    return p


def h2(doc, text):
    p = doc.add_paragraph(style="Heading 2")
    pf = p.paragraph_format
    pf.space_before = Pt(13)
    pf.space_after = Pt(5)
    pf.keep_with_next = True
    r = p.add_run(text)
    run_font(r, size=12.5, bold=True, color=SECONDARY)
    return p


def h3(doc, text):
    p = doc.add_paragraph(style="Heading 3")
    pf = p.paragraph_format
    pf.space_before = Pt(9)
    pf.space_after = Pt(3)
    pf.keep_with_next = True
    r = p.add_run(text)
    run_font(r, size=10.5, bold=True, color=PRIMARY)
    return p


def callout(doc, label, body, fill=PALE, accent=SECONDARY, space_after=10):
    t = doc.add_table(rows=1, cols=1)
    t.alignment = 1
    no_borders(t)
    no_split(t.rows[0])
    cell_margins(t, top=110, bottom=110, left=170, right=150)
    c = t.rows[0].cells[0]
    shade(c, fill)
    c.text = ""
    p = c.paragraphs[0]
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.08
    r = p.add_run(label.upper())
    run_font(r, size=7.8, bold=True, color=accent)
    spacing(r, 24)
    p2 = c.add_paragraph()
    p2.paragraph_format.space_after = Pt(0)
    p2.paragraph_format.line_spacing = 1.1
    r2 = p2.add_run(body)
    run_font(r2, size=9.5, color=INK)
    fixed_layout(t, [CONTENT_W])
    cell_borders(c, color=accent, sz=18, sides=("left",))
    if space_after:
        spacer(doc, space_after)
    return t


def field(paragraph, instr, placeholder=""):
    r = paragraph.add_run()
    r._r.append(el("w:fldChar", **{"w:fldCharType": "begin"}))
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = instr
    r._r.append(it)
    r._r.append(el("w:fldChar", **{"w:fldCharType": "separate"}))
    if placeholder:
        t = OxmlElement("w:t")
        t.text = placeholder
        r._r.append(t)
    r._r.append(el("w:fldChar", **{"w:fldCharType": "end"}))


def hyperlink(paragraph, url, text, size=8.5, color="1F5C99"):
    part = paragraph.part
    r_id = part.relate_to(url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True)
    h = OxmlElement("w:hyperlink")
    h.set(qn("r:id"), r_id)
    new_run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    rf = OxmlElement("w:rFonts")
    for a in ("w:ascii", "w:hAnsi", "w:cs"):
        rf.set(qn(a), BODY)
    rpr.append(rf)
    sz = OxmlElement("w:sz"); sz.set(qn("w:val"), str(int(size * 2))); rpr.append(sz)
    col = OxmlElement("w:color"); col.set(qn("w:val"), color); rpr.append(col)
    u = OxmlElement("w:u"); u.set(qn("w:val"), "single"); rpr.append(u)
    new_run.append(rpr)
    t = OxmlElement("w:t"); t.text = text; t.set(qn("xml:space"), "preserve")
    new_run.append(t)
    h.append(new_run)
    paragraph._p.append(h)


def base_document():
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = BODY
    st.font.size = Pt(10.5)
    st.font.color.rgb = RGBColor.from_string(INK)
    rpr = st.element.get_or_add_rPr()
    rf = OxmlElement("w:rFonts")
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), BODY)
    rpr.append(rf)
    st.paragraph_format.space_after = Pt(7)
    st.paragraph_format.line_spacing = 1.13

    for name, size, color in (("Heading 1", 17, PRIMARY), ("Heading 2", 12.5, SECONDARY)):
        hs = doc.styles[name]
        hs.font.name = BODY
        hs.font.size = Pt(size)
        hs.font.bold = True
        hs.font.color.rgb = RGBColor.from_string(color)
        hs.font.italic = False

    for s in ("List Bullet", "List Number"):
        bs = doc.styles[s]
        bs.font.name = BODY
        bs.font.size = Pt(10.5)
        bs.paragraph_format.space_after = Pt(3)

    # TOC entries: tight spacing so the contents fit on one page
    try:
        from docx.enum.style import WD_STYLE_TYPE
        try:
            toc = doc.styles["TOC 1"]
        except KeyError:
            toc = doc.styles.add_style("TOC 1", WD_STYLE_TYPE.PARAGRAPH)
            toc.base_style = doc.styles["Normal"]
        toc.font.name = BODY
        toc.font.size = Pt(10)
        toc.font.color.rgb = RGBColor.from_string(INK)
        toc.paragraph_format.space_before = Pt(4)
        toc.paragraph_format.space_after = Pt(4)
        toc.paragraph_format.line_spacing = 1.0
    except Exception:
        pass

    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(1.8)
    sec.left_margin = Cm(2.2)
    sec.right_margin = Cm(2.2)
    sec.header_distance = Cm(1.0)
    sec.footer_distance = Cm(0.9)
    sec.different_first_page_header_footer = True

    # running footer
    fp = sec.footer.paragraphs[0]
    fp.alignment = 2
    ppr = fp._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    bdr.append(el("w:top", **{"w:val": "single", "w:sz": 4, "w:space": 6, "w:color": RULE}))
    ppr.append(bdr)
    r = fp.add_run("Model Evaluation & Reporting Strategy  ·  Week 5 of 5  ·  ")
    run_font(r, size=7.8, color=MUTED)
    field(fp, "PAGE", "1")
    r2 = fp.add_run(" / ")
    run_font(r2, size=7.8, color=MUTED)
    field(fp, "NUMPAGES", "1")
    for run in fp.runs:
        run_font(run, size=7.8, color=MUTED)

    hp = sec.header.paragraphs[0]
    hp.alignment = 0
    r3 = hp.add_run("JUNIOR DATA SCIENTIST INTERNSHIP  ·  NAGPUR")
    run_font(r3, size=7.3, color=MUTED, bold=True)
    spacing(r3, 30)
    return doc


def figure(doc, path, width_cm=CONTENT_W, caption_text=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = bool(caption_text)
    p.add_run().add_picture(str(path), width=Cm(width_cm))
    if caption_text:
        caption(doc, caption_text, label="Figure")
    else:
        spacer(doc, 8)
    return p


def code_block(doc, lines, size=7.8, fill="F4F6F3", space_after=8):
    """Monospaced, shaded block for schemas, config and log extracts."""
    t = doc.add_table(rows=1, cols=1)
    t.alignment = 1
    no_borders(t)
    no_split(t.rows[0])
    cell_margins(t, top=90, bottom=90, left=150, right=120)
    c = t.rows[0].cells[0]
    shade(c, fill)
    c.text = ""
    first = True
    for line in lines:
        p = c.paragraphs[0] if first else c.add_paragraph()
        first = False
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(line if line else " ")
        run_font(r, size=size, name="Consolas", color=INK)
    fixed_layout(t, [CONTENT_W])
    cell_borders(c, color=RULE, sz=4)
    if space_after:
        spacer(doc, space_after)
    return t


def kpi_cards(doc, items, cols=4, space_after=8):
    """A row of metric cards: (label, value, note) triples."""
    t = doc.add_table(rows=1, cols=cols)
    no_borders(t)
    cell_margins(t, top=100, bottom=100, left=110, right=80)
    for i, (label, value, note) in enumerate(items):
        c = t.rows[0].cells[i]
        shade(c, PALE)
        c.text = ""
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(label.upper())
        run_font(r, size=6.9, bold=True, color=SECONDARY)
        spacing(r, 24)
        p2 = c.add_paragraph()
        p2.paragraph_format.space_after = Pt(2)
        p2.paragraph_format.line_spacing = 1.0
        r2 = p2.add_run(value)
        run_font(r2, size=17, bold=True, color=PRIMARY)
        p3 = c.add_paragraph()
        p3.paragraph_format.space_after = Pt(0)
        p3.paragraph_format.line_spacing = 1.02
        r3 = p3.add_run(note)
        run_font(r3, size=7.0, color=MUTED)
    fixed_layout(t, [CONTENT_W / cols] * cols)
    if space_after:
        spacer(doc, space_after)
    return t


def before_after(doc, before_title, before_rows, after_title, after_rows,
                 widths=(8.3, 8.3)):
    """Two stacked mini-tables: raw state and cleaned state of the same case."""
    table(doc, [before_title], [tuple(r) for r in before_rows],
          [widths[0]], size=8.0, caption_text=None)
    table(doc, [after_title], [tuple(r) for r in after_rows],
          [widths[1]], size=8.0, caption_text=None)
