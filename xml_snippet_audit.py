import re
import zipfile
from pathlib import Path

xml = zipfile.ZipFile(Path(r"e:/projects/thesis_project_v2/main_updated.docx")).read(
    "word/document.xml"
).decode("utf-8")

needles = [
    "0.00126",
    "۰.۰۰۱۲۶",
    "0.0126",
    "۰.۰۱۲۶",
    "0.9989",
    "۰.۹۹۸۹",
    "98.7",
    "۹۸.۷",
    "99.60%",
    "33.46%",
    "33. 46",
    "99. 6",
    "همبستگی کاهش",
    "کاهش همبستگی از",
    "۳۳.۴۶%",
    "۲۶.۳۴٪",
    "30.19",
    "94.92",
]

lines = []
for needle in needles:
    idx = 0
    n = 0
    while True:
        i = xml.find(needle, idx)
        if i == -1:
            break
        snippet = xml[max(0, i - 200) : i + len(needle) + 200]
        snippet = re.sub(r"<[^>]+>", " ", snippet)
        snippet = re.sub(r"\s+", " ", snippet).strip()
        lines.append(f"=== {needle} (#{n+1}) ===")
        lines.append(snippet)
        n += 1
        idx = i + 1
    if n:
        lines.append(f"count: {n}\n")

# Also extract all table row texts containing percent or correlation
rows = re.findall(r"<w:tr[\s>][\s\S]*?</w:tr>", xml)
for ri, row in enumerate(rows):
    text = re.sub(r"<[^>]+>", " ", row)
    text = re.sub(r"\s+", " ", text).strip()
    if any(k in text for k in ["همبستگی", "0.9989", "0.0126", "0.00126", "98.7", "30.19", "94.92", "7.9993", "26.34", "32.91", "فرضیه", "شاهد عددی"]):
        lines.append(f"ROW {ri}: {text[:400]}")

Path(r"e:/projects/thesis_project_v2/xml_snippet_audit.txt").write_text(
    "\n".join(lines), encoding="utf-8"
)
print("done", len(lines))
