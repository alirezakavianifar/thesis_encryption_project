"""Direct XML replacement inside docx zip archive."""
import os
import shutil
import tempfile
import zipfile
from pathlib import Path

SRC = Path(r"e:\projects\thesis_project_v2\main_updated.docx")

REPLACEMENTS = {
    "6.2138 → 7.9993": "7.2542 → 7.9993",
    "6.7990 → 7.9993": "7.1491 → 7.9993",
    "6.7178 → 7.9993": "5.8825 → 7.9993",
    "7.7522 → 7.9993": "1.0000 → 7.9993",
    "7.4744 → 7.9993": "7.5754 → 7.9993",
    "7.7067 → 7.9994": "7.2855 → 7.9994",
    "7.0583 → 7.9994": "7.9931 → 7.9994",
    "7.4963 → 7.9992": "7.9931 → 7.9992",
    "7.3388 → 7.9993": "7.6718 → 7.9993",
    "6.9207 → 7.9993": "7.6075 → 7.9993",
    "7.4136 → 7.9993": "7.6398 → 7.9993",
    "7.2104 → 7.9993": "6.3472 → 7.9993",
    "از ۶.۵۷ به ۷.۹۹۹۳ بیت": "از ۶.۷۶ به ۷.۹۹۹۳ بیت",
    "آنتروپی میانگین ~۶.۵۷ بیت": "آنتروپی میانگین ~۶.۷۶ بیت",
    "مقادیر تصویر Airplane (۲۱.۲%)": "مقادیر تصویر Airplane (۲۶.۳۴٪)",
    "Baboon ۳۱.۳٪، Tree: ۳۱.۱٪": "Baboon ۳۰.۲۰٪، Tree: ۳۱.۳۱٪",
    (
        "NPCR=99.46%برای تصویر Baboon در محدوده عملکرد روش‌های مرجع قرار دارد."
    ): (
        "NPCR تا ۹۹.۴۸٪ برای تصویر Peppers و میانگین ۹۴.۹۲٪ در محدوده عملکرد روش‌های مرجع قرار دارد."
    ),
    "30/19": "30.19",
    "94/91": "94.92",
    "7/9993": "7.9993",
}


def patch_docx(target: Path) -> int:
    tmpdir = Path(tempfile.mkdtemp())
    total = 0
    try:
        with zipfile.ZipFile(target, "r") as zin:
            zin.extractall(tmpdir)
        xml_path = tmpdir / "word" / "document.xml"
        xml = xml_path.read_text(encoding="utf-8")
        for old, new in REPLACEMENTS.items():
            count = xml.count(old)
            if count:
                xml = xml.replace(old, new)
                total += count
        xml_path.write_text(xml, encoding="utf-8")
        out_tmp = target.with_suffix(".tmp.docx")
        with zipfile.ZipFile(out_tmp, "w", zipfile.ZIP_DEFLATED) as zout:
            for root, _, files in os.walk(tmpdir):
                for name in files:
                    fp = Path(root) / name
                    arc = fp.relative_to(tmpdir).as_posix()
                    zout.write(fp, arc)
        out_tmp.replace(target)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    return total


if __name__ == "__main__":
    n = patch_docx(SRC)
    print(f"Patched {SRC.name}: {n} replacements")
