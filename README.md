# Thesis Encryption Project

Color image encryption using the Chen chaotic system and nine exponential chaotic maps (ECM).

## Repository Layout

| Path | Description |
|------|-------------|
| `scripts/` | Dedicated Word document conversion scripts |
| `scripts/convert_to_word.ps1` | Master conversion script (LaTeX $\rightarrow$ Word DOCX & PDF) |
| `scripts/build.py` | LaTeX preprocessing, section numbering, and Pandoc converter |
| `scripts/make_reference.py` | OpenXML Bidi reference document generator |
| `scripts/postprocess.py` | OpenXML bidi enforcement, RTL list indents, and dynamic TOC generator |
| `scripts/projectcfg.py` | Path and environment configuration |
| `thesis_latex_source/` | Modular XeLaTeX thesis source (Persian, xepersian) |
| `thesis_latex_source/appendix_code.py` | Appendix Python source (included in the PDF) |
| `thesis_latex_source/build_appendix_notebook.py` | Builds `thesis_appendix.ipynb` from `appendix_code.py` |
| `thesis_latex_source/thesis_appendix.ipynb` | Runnable notebook with Persian notes and embedded results |
| `thesis_latex_source/thesis_appendix.py` | VS Code-compatible interactive Python script version of the notebook |
| `thesis_latex_source/images/` | Test images and Chapter 4 figures for the PDF |
| `thesis_latex_source/outputs/` | Generated experiment outputs |
| `main_updated.docx` | Generated Word version of the thesis |

## Build the Word Document (.docx & .pdf)

Run the dedicated conversion script inside the `scripts/` folder:

```powershell
powershell.exe -ExecutionPolicy Bypass -File ".\scripts\convert_to_word.ps1"
```

This pipeline automatically:
1. Generates `reference.docx` with Persian B Lotus / Calibri fonts and OpenXML Bidi defaults.
2. Pre-processes XeLaTeX files with automatic Persian section numbering (`۱-۱`, `۲-۱`, `۴-۵`, etc.) and non-breaking dimensions (`1280 × 720`).
3. Runs Pandoc to produce an intermediate `.docx`.
4. Enforces OpenXML Right-to-Left (`<w:bidi w:val="1"/>` and `<w:rtl w:val="1"/>`) at all document levels.
5. Formats list indents, table captions, and native Word field instructions (`TOC`, `LOT`, `LOF`).
6. Dynamically harvests body page numbers and builds formatted Table of Contents with dot leaders (`..................`).
7. Outputs `thesis_latex_source/word-build/thesis.docx` and `main_updated.docx`.

## Build the PDF (XeLaTeX)

```powershell
cd thesis_latex_source
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

Requires XeLaTeX, xepersian, and fonts in `thesis_latex_source/` (`BLotus.ttf`, `BLotusBd.ttf`, etc.).

## Run the Appendix Notebook

```powershell
cd thesis_latex_source
python build_appendix_notebook.py
jupyter nbconvert --to notebook --execute thesis_appendix.ipynb --inplace --ExecutePreprocessor.timeout=600
```

## Remote Repository

https://github.com/alirezakavianifar/thesis_encryption_project.git
