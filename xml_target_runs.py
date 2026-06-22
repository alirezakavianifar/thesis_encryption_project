import re
import zipfile
from pathlib import Path

xml = zipfile.ZipFile(Path(r"e:/projects/thesis_project_v2/main_updated.docx")).read(
    "word/document.xml"
).decode("utf-8")

targets = [
    "همبستگی کاهش از",
    "کاهش همبستگی از",
    "بیش از ۸۲٪",
    "میانگین شدت تغییرات بین",
    "عبارتند از",
    "NPCR &gt; 99",
    "UACI ≈ 33",
    "۰.۰۰۹٪",
    "۹۸.۷٪",
]

lines = []
for target in targets:
    i = xml.find(target)
    if i == -1:
        lines.append(f"NOT FOUND: {target}")
        continue
    chunk = xml[i - 50 : i + 500]
    # extract runs in chunk
    runs = re.findall(r"<w:r[\s\S]*?</w:r>", chunk)
    lines.append(f"===== {target} =====")
    for r in runs:
        rtl = bool(re.search(r"<w:rtl", r))
        texts = "".join(re.findall(r"<w:t[^>]*>([\s\S]*?)</w:t>", r))
        if texts:
            lines.append(f"  rtl={rtl} | {repr(texts)}")

Path("e:/projects/thesis_project_v2/xml_target_runs.txt").write_text(
    "\n".join(lines), encoding="utf-8"
)
print("ok")
