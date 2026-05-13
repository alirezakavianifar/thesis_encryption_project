# LaTeX Thesis Project Structure

This directory contains a modular LaTeX thesis project with separate files for each section. This organization makes it easier to manage and edit large documents.

## File Organization

### Core Files
- **preamble.tex** - Contains all package declarations and LaTeX setup code
  - All package imports
  - Document class declarations
  - Custom command definitions
  - Encoding and language settings

### Master File
- **main.tex** - Master document that includes all sections
  - Sets up the document structure
  - Includes all chapter files
  - Defines document begin/end

### Front Matter
- **01_titlepage.tex** - Title page
  - University name and department
  - Thesis title
  - Author and advisor information
  - University logo

- **02_frontmatter.tex** - Front matter content
  - Committee approval form
  - Dedication
  - Acknowledgments
  - Table of Contents
  - Abstract

### Chapters
- **03_chapter1.tex** - Research Fundamentals (کلیات تحقیق)
  - Problem Statement
  - Importance and Necessity
  - Research Objectives
  - Key Concepts
  - Scientific Contribution
  - Thesis Structure

- **04_chapter2.tex** - Basic Concepts and Literature Review (مفاهیم پایه و پیشینه)
  - Introduction
  - Cryptography Fundamentals
  - Digital Image Encryption
  - Chaos Theory
  - Chaotic Systems Connection
  - Research Background

- **05_chapter3.tex** - Proposed Algorithm Introduction (معرفی الگوریتم پیشنهادی)
  - Introduction
  - Algorithm Description
  - Chaotic Systems Selection
  - Encryption Process
  - Implementation and Analysis
  - Final Architecture

- **06_chapter4.tex** - Implementation (پیاده سازی الگوریتم)
  - Introduction
  - Test Dataset and Experimental Setup
  - Visual Output Analysis
  - Histogram Analysis
  - Entropy Analysis
  - Pixel Correlation Analysis
  - Security Metrics (NPCR and UACI)
  - Execution Time Analysis

- **07_chapter5.tex** - Discussion and Conclusion (بحث و نتیجه‌گیری)
  - Experimental Results Analysis
  - Discussion and Interpretation
  - Comparison with Other Algorithms
  - Final Conclusions
  - Future Research Recommendations

### Original File
- **6a6e478acc1947c1bfecfac3523ed62b.latex** - Original monolithic thesis file (kept for reference)

## How to Compile

To compile the entire thesis, use:

```bash
pdflatex main.tex
# or
xelatex main.tex  # for better Persian/RTL support
```

Or use your preferred LaTeX editor (Overleaf, TeXStudio, Sublime Text + LaTeX, etc.)

## Project Details

**Subject:** Image Encryption using Exponential Chaotic Systems
**Language:** Persian (RTL text)
**Document Class:** Article
**Special Features:**
- Right-to-Left (RTL) text support for Persian
- Advanced package configuration
- Hyperlinks and cross-references
- Table of contents with hyperlinks

## Directory Structure

```
thesis_project/
├── preamble.tex              # LaTeX setup and packages
├── main.tex                  # Master document
├── 01_titlepage.tex          # Title page
├── 02_frontmatter.tex        # Front matter
├── 03_chapter1.tex           # Chapter 1
├── 04_chapter2.tex           # Chapter 2
├── 05_chapter3.tex           # Chapter 3
├── 06_chapter4.tex           # Chapter 4
├── 07_chapter5.tex           # Chapter 5
├── 6a6e478acc1947c1bfecfac3523ed62b.latex  # Original file
├── vertopal_6a6e478acc1947c1bfecfac3523ed62b/  # Media folder
│   └── media/
│       └── image1.jpeg       # University logo
└── README.md                 # This file
```

## Editing Guidelines

### For Individual Chapters
Simply edit the corresponding chapter file (e.g., `03_chapter1.tex`) and recompile `main.tex`.

### Adding New Content
1. Edit the appropriate chapter file
2. Add sections using `\section{}` or `\subsection{}`
3. Recompile the master file

### Common Commands
- `\section{Title}` - Main section heading
- `\subsection{Title}` - Subsection heading
- `\RL{Persian text}` - Right-to-left text for Persian
- `\textbf{}` - Bold text
- `\textit{}` - Italic text
- `\cite{}` - Citations

## Tips for Maintenance

1. **Consistent Formatting** - Use the same style throughout all files
2. **Cross-References** - Use `\label{}` and `\ref{}` for cross-references
3. **Backup** - Keep backups of important files
4. **Version Control** - Consider using Git for version tracking
5. **Line Width** - Keep lines under 80-100 characters for readability

## Compilation Issues

If you encounter Persian/RTL text issues:
- Use `xelatex` instead of `pdflatex`
- Ensure UTF-8 encoding in all files
- Check that Persian fonts are installed on your system

## Related Files

The thesis references media files located in:
- `vertopal_6a6e478acc1947c1bfecfac3523ed62b/media/`

Adjust image paths in `01_titlepage.tex` if this folder structure changes.
