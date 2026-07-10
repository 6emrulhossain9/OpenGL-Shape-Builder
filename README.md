# 🎨 OpenGL Shape Generator

> A modern GUI-based OpenGL shape designer that lets you visually draw shapes and instantly generate C++ OpenGL (GLUT) code.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![OpenGL](https://img.shields.io/badge/OpenGL-GLUT-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📌 Overview

OpenGL Shape Generator is a desktop application built with **Python** and **Tkinter** that helps students and beginners create OpenGL shapes visually instead of manually writing vertex coordinates.

Simply draw your shapes on the canvas, choose colors, and generate ready-to-use **C++ OpenGL (GLUT)** code with a single click.

This project was primarily created for my own OpenGL coursework and personal workflow to save time when designing assignments.

> **Note:** This project was **vibe coded** with AI assistance for personal use. I designed the idea, features, tested the application, and refined it to fit my workflow rather than writing every line manually.

---

# ✨ Features

- 🎨 Modern dark-themed interface
- 🖱️ Interactive drawing canvas
- 📐 Draw multiple shape types:
  - Polygon
  - Line
  - Rectangle
  - Square
  - Triangle
  - Circle
- 🌈 Color picker
- 📍 OpenGL coordinate system preview
- 🔲 Optional Snap-to-Grid
- 📋 Object manager
- ❌ Delete individual shapes
- 🧹 Clear entire canvas
- ⚡ Generate OpenGL C++ (GLUT) code instantly
- 📋 Copy generated code to clipboard
- 💾 Export generated code as a `.cpp` file

---

# 🖥️ Screenshot

> Add a screenshot here after uploading one.

```
/screenshots/main.png
```

---

# 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/opengl-shape-generator.git
```

Go into the project directory:

```bash
cd opengl-shape-generator
```

Run the application:

```bash
python OpenGL_Shape_Generator.py
```

---

# 📦 Requirements

- Python 3.x

No external libraries are required.

The application only uses Python's built-in modules:

- tkinter
- math

---

# 📖 How to Use

1. Launch the application.
2. Select a drawing tool.
3. Draw shapes on the canvas.
4. Pick a color if desired.
5. Continue adding shapes.
6. Click **Generate C++ Code**.
7. Copy the generated code or save it as a `.cpp` file.
8. Compile the exported file using your preferred OpenGL/GLUT setup.

---

# 🛠️ Generated Output

The application exports code similar to:

```cpp
glBegin(GL_POLYGON);
glColor3ub(255,0,0);
glVertex2d(-0.5,0.5);
glVertex2d(0.5,0.5);
glVertex2d(0.5,-0.5);
glVertex2d(-0.5,-0.5);
glEnd();
```

making it much faster to create OpenGL assignments.

---

# 🎯 Why I Built This

While learning OpenGL, I found manually calculating and typing vertex coordinates repetitive and time-consuming.

This tool allows me to visually design shapes and instantly generate the corresponding OpenGL code, making coursework and experimentation significantly faster.

---

# 🔮 Future Improvements

- Undo / Redo
- Move existing shapes
- Resize shapes
- Rotate shapes
- Fill and outline options
- Export project files
- Open existing projects
- Keyboard shortcuts
- Zoom & pan canvas
- Support for additional OpenGL primitives

---

# 🤝 Contributions

This project was built for personal use, but suggestions, bug reports, and pull requests are always welcome.

---

# 📄 License

This project is licensed under the MIT License.

---

## ⭐ If you find this project useful, consider giving it a star!
