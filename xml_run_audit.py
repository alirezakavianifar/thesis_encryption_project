"""Inspect docx XML run structure around numeric/percent passages."""
import re
import zipfile
from pathlib import Path

DOCX = Path(r"e:\projects\thesis_project_v2\main_updated.docx")
NEEDLES = [
    "0.9989",
    "0.0126",
    "0.00126",
    "98.7",
    "82",
    "99.48",
    "26.34",
    "32.91",
    "30.19",
    "94.92",
    "7.9993",
    "UACI",
    "NPCR",
    "همبستگی کاهش",
    "ارزیابی UACI",
    "آزمون NPCR",
]

with zipfile.ZipFile(DOCX) as z:
    xml = z.read("word/document.xml").decode("utf-8")

# split into paragraphs
paras = re.findall(r"<w:p[\s>][\s\S]*?</w:p>", xml)

def para_plain(p):
    return re.sub(r"<[^>]+>", "", p)


def para_runs(p):
    runs = []
    for m in re.finditer(r"<w:r[\s>][\s\S]*?</w:r>", p):
        r = m.group(0)
        rtl = "w:rtl" in r or 'w:val="1"' in r and "rtl" in r
        texts = re.findall(r"<w:t[^>]*>([\s\S]*?)</w:t>", r)
        if texts:
            runs.append(("".join(texts), rtl, r[:120]))
    return runs


out_lines = []
for i, p in enumerate(paras):
    plain = para_plain(p)
    if not any(n in plain for n in NEEDLES):
        continue
    runs = para_runs(p)
    out_lines.append("=" * 80)
    out_lines.append(f"PARA {i}: {plain[:220]}")
    for j, (txt, rtl, _) in enumerate(runs):
        if txt.strip():
            out_lines.append(f"  RUN{j}{' [rtl]' if rtl else ''}: {repr(txt)}")

Path(r"e:\projects\thesis_project_v2\xml_run_audit.txt").write_text(
    "\n".join(out_lines), encoding="utf-8"
)
print("paragraphs:", len(out_lines))
