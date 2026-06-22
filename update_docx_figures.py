"""Replace result figures in main_updated.docx with outputs/figs/."""
import io
import shutil
import zipfile
from pathlib import Path

DOCX = Path(r"e:\projects\thesis_project_v2\main_updated.docx")
FIGS = Path(r"e:\projects\thesis_project_v2\outputs\figs")
BACKUP = DOCX.with_suffix(".docx.bak")

# Embedded media name -> source figure (non-result images left unchanged)
REPLACEMENTS = {
    "word/media/image5.png": FIGS / "fig1_visual.png",
    "word/media/image6.png": FIGS / "fig2_histograms.png",
    "word/media/image8.png": FIGS / "fig3_correlation.png",
    "word/media/image7.png": FIGS / "fig4_entropy.png",
    "word/media/image10.png": FIGS / "fig5_npcr_uaci.png",
    "word/media/image11.png": FIGS / "fig6_time.png",
    "word/media/image9.png": FIGS / "fig7_corr_bars.png",
}


def main():
    for arc, src in REPLACEMENTS.items():
        if not src.exists():
            raise FileNotFoundError(f"Missing figure: {src}")

    shutil.copy2(DOCX, BACKUP)

    buf = io.BytesIO()
    with zipfile.ZipFile(DOCX, "r") as zin:
        with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename in REPLACEMENTS:
                    data = REPLACEMENTS[item.filename].read_bytes()
                    print(
                        f"Replaced {item.filename} "
                        f"<- {REPLACEMENTS[item.filename].name} ({len(data)} bytes)"
                    )
                zout.writestr(item, data)

    DOCX.write_bytes(buf.getvalue())
    print(f"Saved {DOCX.name}")
    print(f"Backup: {BACKUP.name}")


if __name__ == "__main__":
    main()
