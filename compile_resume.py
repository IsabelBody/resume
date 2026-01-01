#!/usr/bin/env python3
"""
Resume compilation script for LaTeX CV.
Compiles resume.tex to PDF using XeLaTeX (required for this resume class).
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

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

def clean_aux_files_before_compile(output_name='IsabelBodyResume'):
    """Clean up auxiliary LaTeX files before compilation to force fresh build."""
    aux_extensions = ['.aux', '.log', '.out', '.fdb_latexmk', '.fls', '.synctex.gz']
    cleaned = []
    
    # Clean files with the output name prefix
    for ext in aux_extensions:
        file_path = Path(f'{output_name}{ext}')
        if file_path.exists():
            try:
                file_path.unlink()
                cleaned.append(file_path.name)
            except Exception:
                pass
    
    # Also clean generic auxiliary files
    for ext in aux_extensions:
        for file in Path('.').glob(f'*{ext}'):
            try:
                if file.name.startswith(output_name):
                    continue  # Already cleaned above
                file.unlink()
                cleaned.append(file.name)
            except Exception:
                pass
    
    if cleaned:
        print(f"[INFO] Cleaned {len(cleaned)} auxiliary file(s) to force fresh compilation")

def compile_resume(force_clean=False):
    """Compile the resume.tex file to PDF."""
    resume_file = Path('resume.tex')
    
    if not resume_file.exists():
        print(f"[ERROR] {resume_file} not found!")
        return False
    
    # Check if class file exists locally
    class_file = Path('resume.cls')
    if not class_file.exists():
        print(f"[WARNING] {class_file} not found in current directory!")
        print("  LaTeX will search system directories, which may use cached versions.")
    
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
    
    output_name = 'IsabelBodyResume'
    
    # Clean auxiliary files before compilation if requested or if force_clean
    if force_clean:
        clean_aux_files_before_compile(output_name)
    
    # Compile with XeLaTeX (typically requires 2 passes for references)
    try:
        print("\nRunning XeLaTeX (first pass)...")
        result1 = subprocess.run(
            ['xelatex', '-interaction=nonstopmode', '-output-directory=.', f'-jobname={output_name}', str(resume_file)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Check log for critical errors
        log_file = Path(f'{output_name}.log')
        has_critical_errors = False
        if log_file.exists():
            log_content = log_file.read_text(encoding='utf-8', errors='ignore')
            # Check for "No pages of output" which indicates compilation failed
            if "No pages of output" in log_content:
                has_critical_errors = True
                print("[ERROR] First pass failed - no pages were generated")
                # Extract relevant error lines
                lines = log_content.split('\n')
                error_lines = [line for line in lines if '!' in line or 'Error' in line or 'Fatal' in line]
                if error_lines:
                    print("\nKey errors from log:")
                    for err_line in error_lines[-10:]:  # Last 10 error lines
                        print(f"  {err_line[:100]}")
        
        if result1.returncode != 0 and has_critical_errors:
            print("\n[ERROR] First compilation pass failed with critical errors!")
            return False
        elif result1.returncode != 0:
            print("[WARNING] First compilation pass had warnings/errors")
            print("Attempting second pass anyway...")
        else:
            print("[OK] First pass completed")
        
        print("\nRunning XeLaTeX (second pass for references)...")
        result2 = subprocess.run(
            ['xelatex', '-interaction=nonstopmode', '-output-directory=.', f'-jobname={output_name}', str(resume_file)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Check log again after second pass
        has_critical_errors = False
        if log_file.exists():
            log_content = log_file.read_text(encoding='utf-8', errors='ignore')
            if "No pages of output" in log_content:
                has_critical_errors = True
        
        # Check if PDF was actually created
        pdf_file = Path(f'{output_name}.pdf')
        if pdf_file.exists() and not has_critical_errors:
            print("\n[SUCCESS] Resume compiled successfully!")
            print(f"Output: {pdf_file}")
            # Show PDF modification time
            mtime = pdf_file.stat().st_mtime
            print(f"PDF last modified: {datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Convert PDF to JPG
            jpg_file = Path(f'{output_name}.jpg')
            print(f"\nGenerating JPG preview...")
            if convert_pdf_to_jpg(pdf_file, jpg_file):
                jpg_mtime = jpg_file.stat().st_mtime
                print(f"JPG last modified: {datetime.fromtimestamp(jpg_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print("[WARNING] JPG generation failed, but PDF compilation succeeded")
            
            return True
        else:
            print("\n[ERROR] Compilation failed. PDF was not created or contains errors.")
            if log_file.exists():
                log_content = log_file.read_text(encoding='utf-8', errors='ignore')
                lines = log_content.split('\n')
                error_lines = [line for line in lines if '!' in line or 'Error' in line or 'Fatal' in line]
                if error_lines:
                    print("\nKey errors from log:")
                    for err_line in error_lines[-15:]:  # Last 15 error lines
                        print(f"  {err_line[:120]}")
            return False
            
    except subprocess.TimeoutExpired:
        print("[ERROR] Compilation timed out")
        return False
    except Exception as e:
        print(f"[ERROR] Error during compilation: {e}")
        return False

def convert_pdf_to_jpg(pdf_path, jpg_path, dpi=150):
    """Convert PDF to JPG image using available tools."""
    pdf_path = Path(pdf_path)
    jpg_path = Path(jpg_path)
    
    if not pdf_path.exists():
        print(f"[ERROR] PDF file not found: {pdf_path}")
        return False
    
    # Delete existing JPG if it exists to ensure clean overwrite
    if jpg_path.exists():
        try:
            jpg_path.unlink()
        except Exception as e:
            print(f"[WARNING] Could not delete existing JPG: {e}")
    
    # Try pdf2image (requires poppler)
    try:
        from pdf2image import convert_from_path
        print(f"Converting PDF to JPG using pdf2image...")
        images = convert_from_path(pdf_path, dpi=dpi)
        if images:
            images[0].save(jpg_path, 'JPEG', quality=95)
            print(f"[OK] JPG generated: {jpg_path}")
            return True
    except ImportError:
        pass
    except Exception as e:
        print(f"[WARNING] pdf2image conversion failed: {e}")
    
    # Try PyMuPDF (fitz)
    try:
        import fitz  # PyMuPDF
        print(f"Converting PDF to JPG using PyMuPDF...")
        doc = fitz.open(pdf_path)
        if len(doc) > 0:
            page = doc[0]
            # Render page to pixmap
            zoom = dpi / 72.0  # Convert DPI to zoom factor
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            # Convert to PIL Image and save as JPEG
            from PIL import Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img.save(jpg_path, 'JPEG', quality=95)
            doc.close()
            print(f"[OK] JPG generated: {jpg_path}")
            return True
    except ImportError:
        pass
    except Exception as e:
        print(f"[WARNING] PyMuPDF conversion failed: {e}")
    
    # Try ImageMagick (external tool)
    try:
        print(f"Attempting to convert PDF to JPG using ImageMagick...")
        result = subprocess.run(
            ['magick', 'convert', '-density', str(dpi), str(pdf_path) + '[0]', '-quality', '95', str(jpg_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0 and jpg_path.exists():
            print(f"[OK] JPG generated: {jpg_path}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    except Exception as e:
        print(f"[WARNING] ImageMagick conversion failed: {e}")
    
    print("[ERROR] Could not convert PDF to JPG. Please install one of:")
    print("  - pdf2image: pip install pdf2image (also requires poppler)")
    print("  - PyMuPDF: pip install PyMuPDF")
    print("  - ImageMagick: https://imagemagick.org/script/download.php")
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
    parser.add_argument('--force-clean', action='store_true', help='Clean auxiliary files before compilation (recommended when class file changes)')
    args = parser.parse_args()
    
    success = compile_resume(force_clean=args.force_clean)
    
    if args.clean and success:
        clean_aux_files()
    
    sys.exit(0 if success else 1)
