# Implementation Plan: Update Figure 4-2 (Histogram Comparison) to Match 7.9973 Entropy

## Analysis Summary & Required Changes

Analysis of **Figure 4-2** reveals that updates are **strictly necessary** for the following reasons:

1. **Entropy Mismatch (8.0000 vs. 7.9973 bits)**:
   - In the current figure, the three "Encrypted" columns (Blue, Green, Red) are rendered as **completely solid, perfectly flat rectangles** ($\text{CV}\% = 0.0\%$).
   - Mathematically, a perfectly flat histogram with identical bin counts across all 256 bins corresponds to an exact entropy of $\log_2(256) = 8.0000\text{ bits}$.
   - Since the thesis was updated to reflect the true/revised entropy of **$7.9973\text{ bits}$** (with realistic statistical fluctuations explained in Chapter 4 text), the encrypted histograms must show natural pseudo-random statistical fluctuations (near-uniform distribution with subtle bin-to-bin variance) rather than an artificial flat block.
2. **Text-Figure Inconsistency in Chapter 4**:
   - Chapter 4 (Section 4.4 and Section 4.5) explicitly discusses "نوسانات آماری طبیعی ناشی از ماهیت ذاتی دنباله‌های شبه‌تصادفی آشوبی" (natural statistical fluctuations of $\approx \pm 1\%$ due to chaotic pseudo-randomness). Retaining a perfectly flat rectangular box creates a visible contradiction for reviewers.
3. **Artifacts in Original Histograms**:
   - The original histogram for *Peppers* (Blue and Green channels) is displayed as an unnatural solid block with a single peak, and *Baboon* Blue has only two isolated spikes. These legacy synthetic artifacts must be replaced with accurate distributions from the test dataset.

---

## User Review Required

> [!IMPORTANT]
> **Dataset Inclusion Choice**: 
> Chapter 4 evaluates 6 images (Airplane, Baboon, Peppers, Tree, Kodak01, Kodak02), whereas Figure 4-2 currently displays 4 images (Airplane, Baboon, Peppers, Tree). 
> - **Option A (Recommended)**: Keep the 4 classic USC-SIPI images (Airplane, Baboon, Peppers, Tree) to maintain compact vertical layout while regenerating their encrypted histograms to reflect realistic 7.9973 entropy.
> - **Option B**: Expand Figure 4-2 to include all 6 images (adding Kodak01 and Kodak02).

---

## Proposed Changes

### Figure Generation & Scripts

#### [MODIFY] [thesis_appendix.py](file:///e:/projects/thesis_project_v2/thesis_latex_source/thesis_appendix.py) / [appendix_code.py](file:///e:/projects/thesis_project_v2/thesis_latex_source/appendix_code.py)
- Update the histogram plotting routines for Figure 4-2:
  - Generate encrypted histograms directly from cipher images without artificial flat-histogram override, reflecting the authentic $7.9973$ entropy distribution with natural chaotic fluctuations.
  - Fix any original channel histogram anomalies so they represent genuine test image distributions.
  - Set proper bin ranges (`bins=256, range=(0, 256)`), axis styling, and clean labels.

#### [NEW] [regenerate_fig2.py](file:///e:/projects/thesis_project_v2/scripts/regenerate_fig2.py)
- Create a standalone Python generation script using the project's chaotic encryption engine to produce the updated high-resolution `fig2_histograms.png` and save it directly to `thesis_latex_source/images/fig2_histograms.png`.

---

### Documentation & Build Artifacts

#### [MODIFY] [06_chapter4.tex](file:///e:/projects/thesis_project_v2/thesis_latex_source/06_chapter4.tex)
- Verify caption, labels, and text references around Figure 4-2 (`\label{fig:histograms}`) to ensure complete alignment with the new visual output.

#### [MODIFY] [postprocess.py](file:///e:/projects/thesis_project_v2/scripts/postprocess.py) / Word Build
- Re-run the build pipeline (`scripts/build.py` / `scripts/convert_to_word.ps1`) to ensure the updated figure is synchronized into both the LaTeX PDF and Word (`.docx`) distributions.

---

## Verification Plan

### Automated Tests & Verification
1. Run `regenerate_fig2.py` via `.\venv\Scripts\python.exe` to generate the new `fig2_histograms.png`.
2. Inspect the generated image using `view_file` to confirm:
   - Encrypted histograms show realistic near-uniform distributions with subtle statistical variance matching $H \approx 7.9973$.
   - Original histograms correctly reflect true image channel distributions.
   - Image resolution, font sizes, and layout are crisp and clear.
3. Build the LaTeX thesis and Word document to confirm figure rendering.

### Manual Verification
- Review the generated figure against Table 4-2 entropy values and Chapter 4 textual descriptions.
