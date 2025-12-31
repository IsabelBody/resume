# Resume

**[View Resume PDF →](IsabelBodyResume.pdf)**

A single-page, one-column resume for data scientists. It uses base LaTeX templates and custom Roboto fonts to provide ease of use and installation when trying to update the resume. The different sections are clearly documented and custom commands are used to provide consistent formatting. The main sections in the resume are summary, experience, education, achievements, skills, and projects.

---

<details>
<summary>Repository Information</summary>

This repository contains my LaTeX resume.

## Setup

### 1. Install LaTeX (Required)

This resume requires **XeLaTeX** to compile. Install one of the following:

**Option A: MiKTeX (Recommended for Windows)**
- Download: https://miktex.org/download
- Install the full distribution
- XeLaTeX will be included

**Option B: TeX Live**
- Download: https://www.tug.org/texlive/
- Install the full distribution

### 2. Python Environment (Optional)

The Python virtual environment is optional and used for the compilation script:

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Compile the Resume

**Option A: Using the Python script (Recommended)**
```bash
python compile_resume.py
```

**Option B: Direct XeLaTeX command**
```bash
xelatex resume.tex
xelatex resume.tex  # Run twice for proper references
```

**Option C: Clean compilation (removes auxiliary files)**
```bash
python compile_resume.py --clean
```

## File Structure

```
.
├── resume.tex          # Main LaTeX file
├── profile.png         # Profile photo
├── cv/                 # Section files
│   ├── summary.tex
│   ├── education.tex
│   ├── experience.tex
│   ├── skills.tex
│   ├── projects.tex
│   └── ...
├── cv/fonts/           # Custom fonts
│   └── ...
├── compile_resume.py   # Compilation script
└── README.md           # This file
```

## Editing Your Resume

1. Edit the main file: `resume.tex` - Personal information and section order
2. Edit section files in `cv/` directory:
   - `cv/experience.tex` - Work experience
   - `cv/education.tex` - Education
   - `cv/skills.tex` - Skills
   - `cv/projects.tex` - Projects
   - etc.

3. Compile after making changes:
   ```bash
   python compile_resume.py
   ```

## Troubleshooting

**"XeLaTeX not found" error:**
- Make sure LaTeX is installed and added to your PATH
- Restart your terminal after installation
- On Windows, MiKTeX usually adds itself to PATH automatically

**Font errors:**
- Make sure the `cv/fonts/` directory contains all required fonts
- XeLaTeX should handle font loading automatically

**Compilation errors:**
- Check the `.log` file for detailed error messages
- Make sure all `\input{}` files exist
- Verify LaTeX syntax in your edits

## Alternative: Using Overleaf

If you prefer online editing:
1. Go to https://www.overleaf.com
2. Upload all files (resume.tex, cv/, fonts/, profile.png)
3. Set compiler to XeLaTeX (Menu → Compiler)
4. Compile and edit online

</details>
