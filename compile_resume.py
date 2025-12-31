#!/usr/bin/env python3
"""
Resume compilation script for LaTeX CV.
Compiles resume.tex to PDF using XeLaTeX (required for this resume class).
"""

import subprocess
import sys
from pathlib import Path

def check_latex_installed():
    """Check if XeLaTeX is installed."""
    import os
    import platform
    
    # First try the command directly (if in PATH)
    try:
        result = subprocess.run(
            ['xelatex', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("[OK] XeLaTeX is installed")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    # Try common MiKTeX installation paths on Windows
    if platform.system() == 'Windows':
        miktex_paths = [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'MiKTeX', 'miktex', 'bin', 'x64', 'xelatex.exe'),
            os.path.join('C:', 'Program Files', 'MiKTeX', 'miktex', 'bin', 'x64', 'xelatex.exe'),
            os.path.join('C:', 'Program Files (x86)', 'MiKTeX', 'miktex', 'bin', 'x64', 'xelatex.exe'),
        ]
        
        for xelatex_path in miktex_paths:
            if os.path.exists(xelatex_path):
                # Add to PATH for this session
                bin_dir = os.path.dirname(xelatex_path)
                current_path = os.environ.get('PATH', '')
                if bin_dir not in current_path:
                    os.environ['PATH'] = bin_dir + os.pathsep + current_path
                    print(f"[OK] Found XeLaTeX at: {bin_dir}")
                    print("  (Added to PATH for this session)")
                return True
    
    # Also check for pdflatex as fallback
    try:
        result = subprocess.run(
            ['pdflatex', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("[WARNING] pdflatex found, but this resume requires XeLaTeX")
            print("  Consider installing MiKTeX or TeX Live for XeLaTeX support")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    return False

def compile_resume():
    """Compile the resume.tex file to PDF."""
    resume_file = Path('resume.tex')
    
    if not resume_file.exists():
        print(f"[ERROR] {resume_file} not found!")
        return False
    
    print(f"Compiling {resume_file}...")
    
    # Check if XeLaTeX is available
    if not check_latex_installed():
        print("\n[ERROR] XeLaTeX is not installed!")
        print("\nTo install LaTeX on Windows:")
        print("   1. Download MiKTeX: https://miktex.org/download")
        print("   2. Or download TeX Live: https://www.tug.org/texlive/")
        print("   3. After installation, restart your terminal and try again")
        print("\nAlternatively, you can use Overleaf online at: https://www.overleaf.com")
        return False
    
    # Compile with XeLaTeX (typically requires 2 passes for references)
    try:
        print("\nRunning XeLaTeX (first pass)...")
        result1 = subprocess.run(
            ['xelatex', '-interaction=nonstopmode', '-output-directory=.', str(resume_file)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result1.returncode != 0:
            print("[WARNING] First compilation pass had warnings/errors")
            print("Attempting second pass anyway...")
        else:
            print("[OK] First pass completed")
        
        print("\nRunning XeLaTeX (second pass for references)...")
        result2 = subprocess.run(
            ['xelatex', '-interaction=nonstopmode', '-output-directory=.', str(resume_file)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Check if PDF was actually created (MiKTeX sometimes returns non-zero for warnings)
        pdf_file = resume_file.with_suffix('.pdf')
        if pdf_file.exists():
            print("\n[SUCCESS] Resume compiled successfully!")
            print(f"Output: {pdf_file}")
            return True
        else:
            print("\n[ERROR] Compilation failed. PDF was not created.")
            if result2.stderr:
                print("\nErrors:")
                print(result2.stderr[-500:])  # Last 500 chars
            return False
            
    except subprocess.TimeoutExpired:
        print("[ERROR] Compilation timed out")
        return False
    except Exception as e:
        print(f"[ERROR] Error during compilation: {e}")
        return False

def clean_aux_files():
    """Clean up auxiliary LaTeX files."""
    aux_extensions = ['.aux', '.log', '.out', '.fdb_latexmk', '.fls', '.synctex.gz']
    cleaned = []
    
    for ext in aux_extensions:
        for file in Path('.').glob(f'*{ext}'):
            try:
                file.unlink()
                cleaned.append(file.name)
            except Exception:
                pass
    
    if cleaned:
        print(f"Cleaned up auxiliary files: {', '.join(cleaned)}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Compile LaTeX resume to PDF')
    parser.add_argument('--clean', action='store_true', help='Clean auxiliary files after compilation')
    args = parser.parse_args()
    
    success = compile_resume()
    
    if args.clean and success:
        clean_aux_files()
    
    sys.exit(0 if success else 1)
