# MATH Competition Problems Viewer

A web application for browsing and solving over 12,500 real competition mathematics problems from the MATH dataset.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Demo

![Demo](https://i.imgur.com/5sZnUiT.gif)

## Features

- Access to 12,500+ authentic competition problems
- Multiple difficulty levels (1-5)
- Seven mathematical categories
- Full LaTeX rendering with MathJax
- Asymptote diagram support with code viewer
- Keyboard shortcuts for faster navigation
- Responsive design

## Prerequisites

- Python 3.8+
- pip

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/math-competition-viewer.git
cd math-competition-viewer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

### Categories

- Prealgebra
- Algebra
- Intermediate Algebra
- Number Theory
- Counting & Probability
- Geometry
- Precalculus

### Keyboard Shortcuts

- `N` - Load next problem
- `S` - Toggle solution visibility
- `C` - Copy problem text

### Diagrams

Geometric problems containing Asymptote diagrams display a placeholder with the option to view the source code. For local rendering, see the optional diagram renderer script.

## Project Structure
```
.
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── render_diagram.py      # Optional Asymptote renderer
├── templates/
│   └── index.html        # Frontend interface
└── diagrams/             # Generated diagrams (not tracked)
```

## API Endpoints

- `GET /` - Main application interface
- `GET /api/question/<category>` - Fetch random problem from category
- `GET /api/stats` - Dataset statistics

## Dataset

This application uses the [competition_math](https://huggingface.co/datasets/qwedsacf/competition_math) dataset from HuggingFace, which contains problems from mathematical competitions including AMC, AIME, and others.

## Optional: Diagram Rendering

To render Asymptote diagrams locally:

1. Install [Asymptote](https://asymptote.sourceforge.io/)
2. Install [Ghostscript](https://ghostscript.com/releases/gsdnld.html)
3. Copy diagram code from the web interface
4. Run `python render_diagram.py`
