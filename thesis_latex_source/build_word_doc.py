import os
import sys
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")

def run_pipeline():
    print("Running thesis Word generation pipeline...")
    for script in ["make_reference.py", "build.py", "postprocess.py"]:
        script_path = os.path.join(SCRIPTS_DIR, script)
        print(f"==> python {script}")
        res = subprocess.run([sys.executable, script_path], cwd=SCRIPTS_DIR)
        if res.returncode != 0:
            raise RuntimeError(f"{script} failed with exit code {res.returncode}")
    print("\nWord build completed successfully.")

if __name__ == "__main__":
    run_pipeline()
