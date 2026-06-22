"""Extract readable paragraphs and table cells from docx for percentage audit."""
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def para_text(p):
    return "".join(t.text or "" for t in p.iter(f"{W}t"))


def extract_docx(path: Path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))

    lines = []
    for el in root.iter():
        if el.tag == f"{W}p":
            t = para_text(el).strip()
            if t:
                lines.append(("P", t))
        elif el.tag == f"{W}tbl":
            for tr in el.iter(f"{W}tr"):
                cells = []
                for tc in tr.iter(f"{W}tc"):
                    cell = " ".join(para_text(p).strip() for p in tc.iter(f"{W}p") if para_text(p).strip())
                    cells.append(cell)
                if any(cells):
                    lines.append(("T", " | ".join(cells)))
    return lines


def audit(path: Path):
    keywords = ["%", "\u066a", "\u062a", "NPCR", "UACI", "0.9989", "0.0126", "0.00126", "98.7", "99.48", "26.34", "30.19", "94.92", "7.9993", "6.76", "0.009"]
    lines = extract_docx(path)
    hits = []
    for kind, text in lines:
        if any(k in text for k in keywords):
            hits.append(f"[{kind}] {text}")
    out = path.with_name(path.stem + "_percent_audit.txt")
    out.write_text("\n".join(hits), encoding="utf-8")
    return len(hits), out


if __name__ == "__main__":
    for name in ["main_updated.docx", "main_updated_corrected.docx"]:
        p = Path(r"e:\projects\thesis_project_v2") / name
        if p.exists():
            n, out = audit(p)
            print(f"{name}: {n} lines -> {out.name}")
