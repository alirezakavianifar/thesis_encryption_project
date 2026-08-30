import os

class Config:
    def __init__(self):
        self.scripts_dir = os.path.dirname(os.path.abspath(__file__))
        self.repo_root = os.path.dirname(self.scripts_dir)
        self.latex_source_dir = os.path.join(self.repo_root, "thesis_latex_source")
        self.word_build_dir = os.path.join(self.latex_source_dir, "word-build")
        
        self.main_tex = os.path.join(self.latex_source_dir, "main.tex")
        self.reference_docx = os.path.join(self.word_build_dir, "reference.docx")
        self.intermediate_docx = os.path.join(self.word_build_dir, "_intermediate.docx")
        self.output_docx = os.path.join(self.word_build_dir, "thesis.docx")
        self.merged_tex = os.path.join(self.word_build_dir, "_thesis_body.tex")
        
        self.font_family_persian = "B Lotus"
        self.font_family_latin = "Calibri"

CFG = Config()
