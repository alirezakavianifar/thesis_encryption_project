# Jupyter Notebook Conventions and Development Guide

## Overview

This document explains conventions for writing bilingual (English + Persian/Farsi) Jupyter notebooks and provides comprehensive guidance on:
- Notebook structure and organization patterns
- Bilingual content conventions
- Programmatic notebook modification techniques
- Environment setup with `uv`
- Notebook execution with `nbconvert`
- Best practices for maintainable notebooks

**Note**: This guide is designed to be generic and applicable to any bilingual notebook project. Replace project-specific references (e.g., `your_notebook.ipynb`, `your_project_name`) with your actual project details.

---

## Notebook Conventions

### 1. **Bilingual Structure (English & Persian)**

The notebook follows a **bilingual approach** with both English and Persian (Farsi) content:

- **English**: Used for code comments, technical documentation, and international accessibility
- **Persian (Farsi)**: Used for:
  - Section headers: `## فاز X: [Phase Name]`
  - Output explanations: `### توضیحات خروجی` (Output Explanations)
  - User-facing documentation and interpretations
  - Right-to-left (RTL) formatted sections using `<div dir="rtl">` HTML tags

**Example Structure:**
```markdown
## فاز ۴: طراحی مدل هزینه
[English content]
### توضیحات خروجی
<div dir="rtl">
[Persian explanation]
</div>
```

### 2. **Phase-Based Organization**

The notebook is organized into **distinct phases** (adapt the number and names to your project):

**Example Phase Structure:**
- **Phase 0**: Project Setup (`فاز ۰: راه‌اندازی پروژه`)
- **Phase 1**: Data Collection (`فاز ۱: جمع‌آوری داده`)
- **Phase 2**: Data Cleaning & EDA (`فاز ۲: پاکسازی داده`)
- **Phase N**: [Your Phase Name] (`فاز N: [Persian Name]`)

Each phase follows a consistent structure:
1. **Phase Header** (Bilingual)
2. **Code Cells** (Implementation)
3. **Output Explanation** (`### توضیحات خروجی`)
4. **Analysis/Interpretation** (Bilingual)

### 3. **Cell Type Patterns**

The notebook uses a **consistent alternation** between markdown and code cells:

- **Markdown Cells**: 
  - Section headers (`##`, `###`)
  - Explanations and interpretations
  - Performance analysis summaries
  - Output descriptions

- **Code Cells**:
  - Import statements and setup
  - Data processing and analysis
  - Visualization generation
  - Results computation

**Pattern**: Typically `[Markdown Header] → [Code] → [Markdown Explanation] → [Code] → ...`

### 4. **Output Explanation Convention**

After each significant code execution, there is a markdown cell with:

- **English Header**: `### Important Note:` or `### Output Explanation:`
- **Persian Header**: `### توضیحات خروجی` (Output Explanations)
- **Bilingual Content**: Explains what the output means, key findings, and interpretations

**Example:**
```markdown
### توضیحات خروجی
<div dir="rtl">
تحلیل اکتشافی داده‌ها (EDA) انجام شد و آمار مقصدها محاسبه گردید...
</div>
```

### 5. **Performance Analysis Format**

Some sections include detailed performance analysis with structured format:

- **Status**: Overall assessment (e.g., "✅ EXCELLENT", "⚠️ WARNING")
- **Performance Metrics**: Quantitative measures
- **Quality Assessment**: Score-based evaluation
- **Issues/Concerns**: Problem identification
- **Recommendations**: Action items
- **Overall Assessment**: Summary conclusion

### 6. **Visualization Conventions**

- Visualizations are saved to `outputs/` directory
- High-resolution output: `dpi=300, bbox_inches='tight'`
- Consistent color schemes and styling
- Bilingual axis labels where appropriate

### 7. **Code Organization**

- **Imports**: Centralized at the beginning
- **Configuration**: Constants defined early (`OUTPUT_DIR`, `data_file`)
- **Modular Design**: Uses custom modules from `src/` package
- **Error Handling**: Includes `try-except` blocks and validation checks
- **Progressive Execution**: Each phase builds on previous results

### 8. **Terminology Consistency**

The notebook maintains consistent terminology throughout:

- **Key Terms**: Define and use consistent technical terms
- **Bilingual Alignment**: Ensure English and Persian terms match conceptually
- **Abbreviations**: Define abbreviations on first use
- **Domain-Specific Terms**: Use standard terminology for your field

**Example:**
- **"Decision Analysis"** (`تحلیل تصمیم`) - NOT "Full Optimization" (`بهینه‌سازی کامل`)
- **"Baseline"** (`خط پایه`) - Initial reference point
- **"Optimal"** (`بهینه`) - Best solution according to criteria

### 9. **Error Handling Patterns**

Code includes defensive programming:

```python
# Check if variable exists before use
if 'variable_name' not in globals() or variable_name is None:
    # Initialize variable
    variable_name = initialize_function()

# Filter invalid values
summary = summary[summary['column'].replace([np.inf, -np.inf], np.nan).notna()]

# Handle missing keys
if 'key' in results_dict:
    value = results_dict['key']
```

### 10. **Documentation Style**

- **Inline Comments**: Explain complex logic
- **Docstrings**: Not used in notebook cells (functions are in `src/` modules)
- **Markdown Explanations**: Detailed interpretations after code execution
- **Bilingual Notes**: Both English and Persian explanations for key concepts

### 11. **Human-Written Style Guidelines**

**Critical Principle**: All code, comments, and descriptions should be written in a natural, human-written style that does not appear AI-generated.

**Code Writing:**
- **Natural Comments**: Write comments as you would explain to a colleague, not as formal documentation
  ```python
  # Bad (AI-like): "This function calculates the optimal transportation mode"
  # Good (Human-like): "Find the cheapest mode that meets our lead time requirement"
  
  # Bad (AI-like): "Initialize the cost model with default parameters"
  # Good (Human-like): "Set up cost model - we'll tweak these numbers later if needed"
  ```

- **Variable Names**: Use natural, contextual names rather than overly descriptive ones
  ```python
  # Bad (AI-like): optimal_transportation_mode_per_destination
  # Good (Human-like): best_mode or optimal_mode
  ```

- **Code Flow**: Write code as you would naturally think through the problem
  ```python
  # Natural flow: Check first, then process
  if data is None:
      print("No data available")
      return
  
  # Process the data
  results = analyze(data)
  ```

**Description Writing:**
- **Conversational Tone**: Write explanations as if talking to a team member
  - ❌ "The following analysis demonstrates the application of..."
  - ✅ "Let's look at what the data tells us about..."
  
- **Natural Transitions**: Use connecting phrases that feel natural
  - ❌ "Furthermore, it should be noted that..."
  - ✅ "Also, we noticed that..." or "One more thing: ..."

- **Personal Voice**: Use first person when appropriate
  - ❌ "It is recommended that the user..."
  - ✅ "I recommend..." or "We should..."

- **Varied Sentence Structure**: Mix short and long sentences naturally
  - ❌ All sentences structured the same way
  - ✅ Natural variation in length and complexity

- **Contextual Explanations**: Reference specific observations, not generic statements
  - ❌ "The results show interesting patterns"
  - ✅ "The results show that destinations over 500km consistently use LTL"

**Persian Text Guidelines:**
- **Natural Persian**: Use conversational Persian, not formal/translated style
  - ❌ "این تحلیل نشان می‌دهد که..." (too formal, translation-like)
  - ✅ "نتیجه‌ها نشون می‌دن که..." or "از این تحلیل می‌بینیم که..." (natural)

- **Cultural Context**: Use expressions that feel natural to Persian speakers
- **Mixed Style**: It's natural to mix formal and informal Persian in technical writing

**Red Flags to Avoid:**
- Overly formal language ("It should be noted that...", "One must consider...")
- Repetitive sentence structures
- Excessive use of transition words ("Furthermore", "Moreover", "Additionally")
- Generic statements without specific context
- Perfect grammar that feels too polished
- Over-explanation of obvious things

**Best Practices:**
1. **Write as you think**: Capture your thought process naturally
2. **Read aloud**: If it sounds robotic when read, rewrite it
3. **Use contractions**: "don't", "can't", "we'll" (in English)
4. **Include imperfections**: Minor variations make text feel human
5. **Context-specific**: Reference actual data, not abstract concepts
6. **Personal touches**: Add brief asides or observations

---

## Common Modification Patterns

### 1. **Adding Explanatory Cells**

**Pattern**: Insert markdown cells to explain complex results or edge cases

**Example Use Cases**:
- Explaining infinite or NaN values in results
- Clarifying methodology choices
- Documenting assumptions
- Providing interpretation guidance

**Implementation**: See "Programmatic Notebook Modification" section below.

### 2. **Terminology Corrections**

**Pattern**: Update terminology for consistency and accuracy

**Common Scenarios**:
- Aligning technical terms with domain standards
- Correcting translation mismatches
- Standardizing abbreviations
- Updating deprecated terms

**Best Practice**: Use find-and-replace scripts for bulk updates.

### 3. **Error Handling Improvements**

**Pattern**: Add defensive checks to prevent runtime errors

**Common Additions**:
- Variable existence checks: `if 'var' not in globals()`
- Infinite value filtering: `.replace([np.inf, -np.inf], np.nan)`
- Key existence checks: `if 'key' in dict`
- Graceful degradation for missing data

**Impact**: Notebooks run successfully without `NameError` or `KeyError` exceptions.

### 4. **Function Call Updates**

**Pattern**: Update deprecated functions or fix API changes

**Common Scenarios**:
- Replacing deprecated functions with current versions
- Updating function signatures
- Fixing parameter passing
- Adding missing imports

### 5. **Dynamic Column/Key Handling**

**Pattern**: Handle variations in data structure

**Example**:
```python
# Check for column existence before use
display_cols = ['col1', 'col2', 'col3']
if 'optional_col' in df.columns:
    display_cols.append('optional_col')
elif 'alternative_col' in df.columns:
    display_cols.append('alternative_col')
```

**Impact**: Handles variations in data structure gracefully.

---

## Summary of Conventions

| Convention | Description | Example |
|------------|-------------|---------|
| **Bilingual** | English + Persian content | `## فاز X` + English explanation |
| **Phase Structure** | 10 phases, consistent format | Header → Code → Explanation |
| **Output Explanations** | `### توضیحات خروجی` after code | Persian explanations in RTL divs |
| **Error Handling** | Defensive checks, validation | `if 'var' not in globals()` |
| **Terminology** | "Decision Analysis" not "Optimization" | `تحلیل تصمیم` |
| **Visualization** | Saved to `outputs/`, high-res | `dpi=300, bbox_inches='tight'` |
| **Code Organization** | Modular, progressive execution | Imports → Config → Analysis |

---

## Best Practices Followed

1. ✅ **Consistent Structure**: Each phase follows same pattern
2. ✅ **Bilingual Accessibility**: Both English and Persian speakers can understand
3. ✅ **Clear Explanations**: Output descriptions help users interpret results
4. ✅ **Defensive Programming**: Handles edge cases and missing data
5. ✅ **Modular Design**: Uses `src/` package for reusable code
6. ✅ **Documentation**: Explanations accompany all major outputs
7. ✅ **Error Prevention**: Checks prevent runtime errors
8. ✅ **Terminology Accuracy**: Uses correct technical terms consistently
9. ✅ **Human-Written Style**: All content written in natural, conversational tone

---

## Project Structure Template

```
your_project/
  ├── notebooks/
  │   └── your_notebook.ipynb
  ├── src/                    # Source code modules
  │   ├── __init__.py
  │   └── [your_modules].py
  ├── data/                   # Input data files
  ├── outputs/               # Generated outputs
  ├── requirements.txt        # Python dependencies
  ├── README.md              # Project documentation
  └── .venv/                 # Virtual environment (created by uv)
```

**Notebook Structure**:
- Organize cells by phases/sections
- Maintain consistent markdown/code alternation
- Track cell counts for reference (e.g., "Phase 1: Cells 0-10")

---

## Notes for Future Development

1. **Maintain Bilingual Structure**: Continue using both English and Persian
2. **Follow Phase Pattern**: Keep consistent structure across phases
3. **Add Explanations**: Always include `### توضیحات خروجی` after significant outputs
4. **Handle Edge Cases**: Continue defensive programming practices
5. **Update Terminology**: Use "Decision Analysis" consistently
6. **Document Changes**: Update this file when making structural changes

---

## Environment Setup with `uv`

### Overview

`uv` is a fast Python package installer and resolver written in Rust. It provides:
- **Fast dependency resolution**: 10-100x faster than pip
- **Virtual environment management**: Built-in venv creation
- **Lock file support**: Reproducible dependency management
- **Cross-platform**: Works on Windows, Linux, and macOS

### Installation

**Install `uv` (if not already installed):**

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Verify installation:**
```bash
uv --version
```

### Creating Virtual Environment

**Basic Command:**
```bash
uv venv
```

This creates a `.venv` directory in the current folder.

**Specify Python Version:**
```bash
uv venv --python 3.11
# or
uv venv --python python3.11
```

**Custom Location:**
```bash
uv venv myenv
# Creates myenv/ directory
```

**Activate Virtual Environment:**

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

**Verify Activation:**
```bash
which python  # Should point to .venv/bin/python (Linux/Mac)
# or
where python   # Windows - should show .venv path
```

### Installing Dependencies

**From requirements.txt:**
```bash
uv pip install -r requirements.txt
```

**Install Individual Packages:**
```bash
uv pip install pandas numpy matplotlib
```

**Install with Version Constraints:**
```bash
uv pip install "pandas>=2.0.0" "numpy>=1.24.0"
```

**Install Development Dependencies:**
```bash
uv pip install -r requirements-dev.txt
```

**Upgrade Packages:**
```bash
uv pip install --upgrade pandas
```

**Install from Lock File (if using pyproject.toml):**
```bash
uv sync  # Installs from uv.lock
```

### Creating requirements.txt

**Generate from Current Environment:**
```bash
uv pip freeze > requirements.txt
```

**Or manually create requirements.txt:**
```txt
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
jupyter>=1.0.0
```

### Using pyproject.toml (Advanced)

**Create pyproject.toml:**
```toml
[project]
name = "your-project"
version = "0.1.0"
dependencies = [
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "matplotlib>=3.7.0",
    "jupyter>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
]
```

**Install with uv:**
```bash
uv sync              # Install all dependencies
uv sync --dev        # Include dev dependencies
uv lock              # Generate uv.lock file
```

### Complete Setup Workflow

**Step-by-Step:**

```bash
# 1. Navigate to project directory
cd /path/to/your/project

# 2. Create virtual environment
uv venv

# 3. Activate virtual environment
# Windows:
.venv\Scripts\Activate.ps1
# Linux/Mac:
source .venv/bin/activate

# 4. Install dependencies
uv pip install -r requirements.txt

# 5. Verify installation
python -c "import pandas; print(pandas.__version__)"

# 6. Install Jupyter (if not in requirements.txt)
uv pip install jupyter

# 7. Launch Jupyter
jupyter notebook
# or
jupyter lab
```

### Managing Multiple Environments

**List Virtual Environments:**
```bash
uv venv list  # Shows all venvs managed by uv
```

**Remove Virtual Environment:**
```bash
# Simply delete the directory
rm -rf .venv  # Linux/Mac
rmdir /s .venv  # Windows
```

### Troubleshooting

**Issue: `uv: command not found`**
- Solution: Add `uv` to PATH or reinstall

**Issue: Virtual environment not activating**
- Solution: Check execution policy (Windows): `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Issue: Package installation fails**
- Solution: Check Python version compatibility, try `uv pip install --upgrade pip`

**Issue: Slow installation**
- Solution: `uv` is already fast, but check network connection

### Comparison: uv vs pip/venv

| Feature | uv | pip/venv |
|---------|----|----------|
| **Speed** | 10-100x faster | Standard speed |
| **Virtual Env** | Built-in (`uv venv`) | Separate tool (`python -m venv`) |
| **Lock Files** | Native support | Requires pip-tools |
| **Dependency Resolution** | Fast Rust-based | Python-based |
| **Cross-platform** | Yes | Yes |

### Best Practices

1. **Always use virtual environments**: Isolate project dependencies
2. **Pin versions in requirements.txt**: Ensure reproducibility
3. **Use `.venv` directory**: Standard location, easy to `.gitignore`
4. **Activate before working**: Always activate venv before running notebooks
5. **Update regularly**: Keep dependencies current for security
6. **Document setup**: Include setup instructions in README.md

---

## Notebook Execution with nbconvert

### Overview

`nbconvert` is a Jupyter tool that converts notebooks to various formats and can execute them programmatically. This is essential for:
- **Automated Testing**: Running notebooks in CI/CD pipelines
- **Batch Processing**: Executing multiple notebooks
- **Output Generation**: Creating executed versions with all outputs
- **Validation**: Ensuring notebooks run without errors

### Basic Usage

**Execute and Save (In-Place):**
```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/transportation_optimization_full.ipynb
```

**Execute and Create New File:**
```bash
jupyter nbconvert --to notebook --execute notebooks/transportation_optimization_full.ipynb --output transportation_optimization_full_executed.ipynb
```

**Execute and Convert to HTML:**
```bash
jupyter nbconvert --to html --execute notebooks/transportation_optimization_full.ipynb
```

### Key Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--to notebook` | Output format (notebook, html, pdf, etc.) | `--to notebook` |
| `--execute` | Execute all cells before conversion | `--execute` |
| `--inplace` | Modify file in place (overwrite original) | `--inplace` |
| `--output` | Output filename | `--output executed.ipynb` |
| `--allow-errors` | Continue execution even if errors occur | `--allow-errors` |
| `--ExecutePreprocessor.timeout` | Cell execution timeout | `--ExecutePreprocessor.timeout=300` |

### Typical Workflow

1. **Development**: Edit notebook in Jupyter/VS Code
2. **Validation**: Run with nbconvert to check for errors
3. **Execution**: Generate fully executed version
4. **Distribution**: Convert to HTML/PDF for sharing

**Example Script:**
```bash
#!/bin/bash
# Execute notebook and generate outputs
cd /path/to/your/project
jupyter nbconvert --to notebook --execute --inplace notebooks/your_notebook.ipynb

# Check exit code
if [ $? -eq 0 ]; then
    echo "Notebook executed successfully"
else
    echo "Notebook execution failed"
    exit 1
fi
```

**Windows PowerShell Script:**
```powershell
# Execute notebook
cd C:\path\to\your\project
jupyter nbconvert --to notebook --execute --inplace notebooks/your_notebook.ipynb

if ($LASTEXITCODE -eq 0) {
    Write-Host "Notebook executed successfully"
} else {
    Write-Host "Notebook execution failed"
    exit 1
}
```

### Error Handling

**With Error Tolerance:**
```bash
jupyter nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.allow_errors=True \
    notebooks/your_notebook.ipynb
```

**With Timeout:**
```bash
jupyter nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.timeout=600 \
    notebooks/your_notebook.ipynb
```

**Windows (single line):**
```powershell
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.allow_errors=True notebooks/your_notebook.ipynb
```

### Output Files

After execution, the notebook contains:
- **Executed Code**: All cells run with outputs
- **Generated Files**: CSV, PNG files in `outputs/` directory
- **Execution Metadata**: Execution counts, timestamps
- **Error Traces**: If any cells fail (if `--allow-errors` used)

---

## Programmatic Notebook Modification with Python

### Overview

Notebooks are JSON files, so they can be modified programmatically using Python's `json` module. This approach is used for:
- **Bulk Updates**: Changing multiple cells at once
- **Pattern Matching**: Finding and updating specific content
- **Cell Injection**: Adding new cells at specific positions
- **Content Replacement**: Updating text in markdown or code cells

### Notebook JSON Structure

A notebook is a JSON object with this structure:
```json
{
  "cells": [
    {
      "cell_type": "markdown" | "code",
      "metadata": {},
      "source": ["line1", "line2", ...]  // or string
    },
    ...
  ],
  "metadata": {...},
  "nbformat": 4,
  "nbformat_minor": 2
}
```

### Basic Reading and Writing

**Read Notebook:**
```python
import json
from pathlib import Path

notebook_path = Path('notebooks/transportation_optimization_full.ipynb')

# Read notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Access cells
cells = notebook['cells']
print(f"Total cells: {len(cells)}")
```

**Write Notebook:**
```python
# Modify notebook...
# ...

# Write back
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)
```

### Common Operations

#### 1. **Iterate Through Cells**

```python
for i, cell in enumerate(notebook['cells']):
    cell_type = cell['cell_type']
    source = cell.get('source', [])
    
    # Handle list or string format
    if isinstance(source, list):
        source_text = ''.join(source)
    else:
        source_text = source
    
    print(f"Cell {i}: {cell_type}")
    print(f"  Content: {source_text[:100]}...")
```

#### 2. **Find Cells by Content**

```python
def find_cells_containing(notebook, search_text):
    """Find cells containing specific text."""
    matches = []
    
    for i, cell in enumerate(notebook['cells']):
        source = cell.get('source', [])
        source_text = ''.join(source) if isinstance(source, list) else source
        
        if search_text in source_text:
            matches.append({
                'index': i,
                'type': cell['cell_type'],
                'preview': source_text[:200]
            })
    
    return matches

# Find cells containing specific text
matches = find_cells_containing(notebook, "your_search_text")
for match in matches:
    print(f"Cell {match['index']}: {match['preview']}")
```

#### 3. **Insert New Cell**

```python
def insert_cell(notebook, cell_index, cell_type, source_content):
    """Insert a new cell at specified index."""
    new_cell = {
        "cell_type": cell_type,
        "metadata": {},
        "source": source_content if isinstance(source_content, list) else [source_content]
    }
    
    notebook['cells'].insert(cell_index, new_cell)
    return notebook

# Insert markdown cell at position 51
new_markdown = """### Important Note: [Your Topic]

**Explanation:**

Your explanation text here...
"""

notebook = insert_cell(notebook, 51, "markdown", new_markdown)
```

#### 4. **Modify Existing Cell**

```python
def modify_cell(notebook, cell_index, new_source):
    """Modify source content of a cell."""
    cell = notebook['cells'][cell_index]
    
    # Convert to list format if needed
    if isinstance(new_source, str):
        cell['source'] = [new_source]
    else:
        cell['source'] = new_source
    
    return notebook

# Update cell 10 with new content
new_content = "print('Updated content')"
notebook = modify_cell(notebook, 10, new_content)
```

#### 5. **Replace Text in Cells**

```python
def replace_in_cells(notebook, old_text, new_text, cell_type=None):
    """Replace text across all cells (optionally filtered by type)."""
    modified = False
    
    for cell in notebook['cells']:
        # Filter by cell type if specified
        if cell_type and cell['cell_type'] != cell_type:
            continue
        
        source = cell.get('source', [])
        source_text = ''.join(source) if isinstance(source, list) else source
        
        if old_text in source_text:
            new_source_text = source_text.replace(old_text, new_text)
            cell['source'] = [new_source_text] if not isinstance(source, list) else new_source_text.split('\n')
            modified = True
    
    return notebook, modified

# Replace terminology
notebook, changed = replace_in_cells(
    notebook, 
    "بهینه‌سازی کامل", 
    "تحلیل تصمیم",
    cell_type="markdown"
)
print(f"Replaced in {changed} cells")
```

#### 6. **Add Code Cell with Error Handling**

```python
def insert_code_cell_with_check(notebook, cell_index, code, check_variable=None):
    """Insert code cell with defensive variable checking."""
    if check_variable:
        code_with_check = f"""# Initialize {check_variable} if not already created
if '{check_variable}' not in globals() or {check_variable} is None:
    {code}
else:
    print(f"{check_variable} already exists, skipping initialization")
"""
    else:
        code_with_check = code
    
    new_cell = {
        "cell_type": "code",
        "metadata": {},
        "source": code_with_check.split('\n')
    }
    
    notebook['cells'].insert(cell_index, new_cell)
    return notebook

# Insert initialization code with check
code = """your_variable = your_function(your_params)
print("Variable initialized")
"""

notebook = insert_code_cell_with_check(
    notebook, 
    27, 
    code, 
    check_variable="your_variable"
)
```

### Complete Example: Adding Explanation Cells

```python
#!/usr/bin/env python3
"""Add explanation cells to notebook."""
import json
from pathlib import Path

notebook_path = Path('notebooks/your_notebook.ipynb')

# Read notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Find cell index after target section (search for specific text)
target_index = None
for i, cell in enumerate(notebook['cells']):
    source = ''.join(cell.get('source', []))
    if 'Your Search Text Here' in source:  # Replace with your search text
        target_index = i + 1
        break

if target_index:
    # English explanation cell
    english_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Important Note: [Your Topic]\n",
            "\n",
            "**Explanation:**\n",
            "\n",
            "Your explanation text here...\n"
        ]
    }
    
    # Persian explanation cell
    persian_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "<div dir=\"rtl\">\n",
            "\n",
            "### نکته مهم: [موضوع شما]\n",
            "\n",
            "**توضیح:**\n",
            "\n",
            "متن توضیحات شما اینجا...\n",
            "\n",
            "</div>\n"
        ]
    }
    
    # Insert both cells
    notebook['cells'].insert(target_index, english_cell)
    notebook['cells'].insert(target_index + 1, persian_cell)
    
    # Write back
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, ensure_ascii=False, indent=1)
    
    print(f"Inserted explanation cells at index {target_index}")
else:
    print("Target location not found")
```

### Best Practices

1. **Always Backup**: Create backup before modifying
   ```python
   import shutil
   shutil.copy(notebook_path, f"{notebook_path}.backup")
   ```

2. **Handle Encoding**: Use `encoding='utf-8'` for Persian text
   ```python
   with open(notebook_path, 'r', encoding='utf-8') as f:
       notebook = json.load(f)
   ```

3. **Preserve Format**: Use `indent=1` and `ensure_ascii=False`
   ```python
   json.dump(notebook, f, ensure_ascii=False, indent=1)
   ```

4. **Validate Structure**: Check cell types and required fields
   ```python
   required_fields = ['cell_type', 'metadata', 'source']
   for cell in notebook['cells']:
       assert all(field in cell for field in required_fields)
   ```

5. **Source Format**: Handle both list and string formats
   ```python
   source = cell.get('source', [])
   if isinstance(source, list):
       source_text = ''.join(source)
   else:
       source_text = source
   ```

### Comparison: edit_notebook Tool vs Direct Python

| Approach | Pros | Cons | Use Case |
|----------|------|------|----------|
| **edit_notebook Tool** | - Type-safe<br>- Handles encoding<br>- Validates structure | - Limited to Cursor IDE<br>- Less flexible | Single cell edits |
| **Direct Python JSON** | - Full control<br>- Batch operations<br>- Scriptable | - Manual validation<br>- More error-prone | Bulk modifications |

### Workflow Integration

**Typical Workflow:**
1. **Edit in IDE**: Use `edit_notebook` for single changes
2. **Bulk Updates**: Use Python scripts for pattern-based changes
3. **Validation**: Run `nbconvert --execute` to test
4. **Commit**: Save changes to version control

---

## Quick Reference

### Setup Checklist

- [ ] Install `uv`: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] Create virtual environment: `uv venv`
- [ ] Activate virtual environment: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\Activate.ps1` (Windows)
- [ ] Install dependencies: `uv pip install -r requirements.txt`
- [ ] Install Jupyter: `uv pip install jupyter`
- [ ] Launch Jupyter: `jupyter notebook` or `jupyter lab`

### Writing Style Checklist

- [ ] **Natural Language**: All descriptions use conversational, human-written tone
- [ ] **No AI Patterns**: Avoid overly formal language, repetitive structures, generic statements
- [ ] **Context-Specific**: Reference actual data and observations, not abstract concepts
- [ ] **Personal Voice**: Use "I", "we", "let's" when appropriate
- [ ] **Varied Structure**: Mix sentence lengths and styles naturally
- [ ] **Read Aloud Test**: Content sounds natural when read aloud

### Execution Checklist

- [ ] Activate virtual environment
- [ ] Run notebook: `jupyter nbconvert --to notebook --execute --inplace notebooks/your_notebook.ipynb`
- [ ] Verify outputs generated in `outputs/` directory
- [ ] Check for errors in execution log

### Modification Checklist

- [ ] Backup notebook: `cp your_notebook.ipynb your_notebook.ipynb.backup`
- [ ] Identify target cells (by content or index)
- [ ] Use appropriate tool:
  - Single cell: Use IDE `edit_notebook` tool
  - Bulk changes: Use Python JSON scripts
- [ ] Test modifications: Run with `nbconvert`
- [ ] Verify bilingual consistency
- [ ] Update documentation if needed

---

## Conclusion

This guide provides a comprehensive framework for developing and maintaining bilingual Jupyter notebooks. The conventions ensure consistency, the tools enable efficient workflows, and the best practices promote maintainability.

**Key Tools Summary:**
- **uv**: Fast virtual environment and dependency management
- **nbconvert**: Automated notebook execution and validation
- **Python JSON**: Programmatic bulk modifications
- **edit_notebook**: IDE-based single cell edits

**Adaptation Notes:**
- Replace project-specific references with your actual project details
- Adjust phase structure to match your project's organization
- Customize terminology and conventions to your domain
- Modify examples to reflect your specific use cases
- **Always write in natural, human style** - avoid AI-generated patterns in both code comments and markdown descriptions

Together, these tools and conventions enable efficient development, testing, and maintenance of bilingual technical notebooks.
