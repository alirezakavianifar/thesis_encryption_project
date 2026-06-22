"""Compare figures embedded in main_updated.docx vs outputs/figs/."""
import hashlib
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

DOCX = Path(r"e:\projects\thesis_project_v2\main_updated.docx")
FIGS = Path(r"e:\projects\thesis_project_v2\outputs\figs")

# Hash output figures
out_hashes = {}
for p in sorted(FIGS.glob("*.png")):
    h = hashlib.md5(p.read_bytes()).hexdigest()
    out_hashes[p.name] = h
    print(f"OUTPUT {p.name}: {h}")

print()

with zipfile.ZipFile(DOCX) as z:
    rid_map = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', z.read("word/_rels/document.xml.rels").decode("utf-8")))
    doc = z.read("word/document.xml").decode("utf-8")

    media_hashes = {}
    for name in sorted(z.namelist()):
        if name.startswith("word/media/") and name.endswith(".png"):
            data = z.read(name)
            h = hashlib.md5(data).hexdigest()
            media_hashes[name.split("/")[-1]] = (h, len(data))
            match = [k for k, v in out_hashes.items() if v == h]
            print(f"DOCX {name.split('/')[-1]}: {h} size={len(data)} -> {match or 'NO MATCH'}")

    # Map images to nearby captions
    ns = {
        "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    }
    root = ET.fromstring(doc)
    body = root.find("w:body", ns)
    paras = body.findall("w:p", ns)

    def para_text(p):
        return "".join(t.text or "" for t in p.findall(".//w:t", ns))

    print("\n=== Image placements ===")
    for i, p in enumerate(paras):
        embeds = [
            e.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
            for e in p.findall(".//a:blip", ns)
        ]
        embeds = [e for e in embeds if e]
        if not embeds:
            continue
        cap = ""
        for j in range(i + 1, min(i + 5, len(paras))):
            t = para_text(paras[j]).strip()
            if t.startswith("شکل") or "4-" in t:
                cap = t[:150]
                break
        for e in embeds:
            target = rid_map.get(e, e)
            fname = target.split("/")[-1]
            h = media_hashes.get(fname, ("?", 0))[0]
            match = [k for k, v in out_hashes.items() if v == h]
            print(f"  {fname} -> {match or 'STALE'} | {cap}")
