# Resume

![Resume Preview](IsabelBodyResume.jpg)

**[View Resume PDF →](IsabelBodyResume.pdf)**

A single-page, one-column LaTeX resume template with custom Roboto fonts. Sections are modularized for easy editing.

## Quick Start

### Install LaTeX

This resume requires **XeLaTeX**. Install one of:

- **MiKTeX** (Windows): https://miktex.org/download
- **TeX Live** (All platforms): https://www.tug.org/texlive/

### Compile

```bash
python compile_resume.py
```

Or manually:
```bash
xelatex resume.tex
xelatex resume.tex  # Run twice for references
```

## File Structure

```
.
├── resume.tex          # Main LaTeX file
├── resume.cls          # Resume class file
├── cv/                 # Section files
│   ├── summary.tex
│   ├── experience.tex
│   ├── education.tex
│   ├── achievements.tex
│   ├── skills.tex
│   ├── projects.tex
│   ├── certificates.tex
│   ├── languages.tex
│   └── fonts/         # Custom Roboto fonts
├── compile_resume.py  # Compilation script
└── README.md
```

## Editing

- **Main file**: `resume.tex` - Personal info and section order
- **Sections**: Edit files in `cv/` directory
- **Compile**: Run `python compile_resume.py` after changes

## Troubleshooting

**XeLaTeX not found:**
- Ensure LaTeX is installed and in PATH
- Restart terminal after installation

**Compilation errors:**
- Check `.log` file for details
- Verify all `\input{}` files exist

**Alternative:** Use [Overleaf](https://www.overleaf.com) - upload all files and set compiler to XeLaTeX
