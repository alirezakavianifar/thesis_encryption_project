# Thesis Encryption Project

Color image encryption using Chen chaotic system and nine exponential chaotic maps (ECM).

## Repository layout

| Path | Description |
|------|-------------|
| `thesis_latex_source/` | Modular XeLaTeX thesis (Persian, xepersian) |
| `main_updated.docx` | Updated Word thesis document |
| `code.ipynb` | Algorithm implementation and evaluation |
| `outputs/` | Generated figures and `results.pkl` |
| `sync_docx_to_latex.py` | Sync docx content into chapter `.tex` files |

## Build the PDF

```powershell
cd thesis_latex_source
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

Requires XeLaTeX, xepersian, and fonts in `thesis_latex_source/` (`BLotus.ttf`, `BLotusBd.ttf`, etc.).

## Remote

https://github.com/alirezakavianifar/thesis_encryption_project.git
