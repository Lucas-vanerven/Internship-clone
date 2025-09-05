# C4 Model Diagrams

This directory contains PlantUML diagrams representing the C4 model for the Cronbach's Alpha Web Application.

## Files

- **c4-level1-context.puml** - System Context diagram showing how the application fits in the broader ecosystem
- **c4-level2-container.puml** - Container diagram showing the high-level technology containers
- **c4-level3-frontend-components.puml** - Component diagram for the Vue.js frontend
- **c4-level3-backend-components.puml** - Component diagram for the FastAPI backend
- **c4-level3-statistics-components.puml** - Component diagram for the statistical functions
- **c4-level4-code-example.puml** - Code-level diagram showing the internal structure of the Cronbach's alpha function

## Quick Start 🚀

### 1. VS Code Extension (Recommended)
The PlantUML extension is installed and ready to use:
- Open any `.puml` file
- Press `Alt+D` to preview the diagram
- Or right-click → "PlantUML: Preview Current Diagram"

### 2. Generate PNG Images
```powershell
python generate-png-diagrams.py
```
This creates PNG images and an HTML viewer at `generated-png/index.html`

### 3. Generate ASCII Art
```powershell
python generate-ascii-diagrams.py
```
This creates text-based diagrams in the `ascii-diagrams` folder

## Available Scripts

### `generate-png-diagrams.py`
- Generates PNG images from all `.puml` files
- Uses the online PlantUML server
- Creates an HTML viewer for easy browsing
- Output: `generated-png/` directory

### `generate-ascii-diagrams.py`
- Creates ASCII art representations
- Perfect for documentation or terminals
- Output: `ascii-diagrams/` directory

### `extract-from-markdown.py`
- Extracts PlantUML code from `C4_MODEL.md`
- Keeps `.puml` files in sync with the main documentation
- Useful when updating the markdown file

## How to Use

### VS Code Integration ✅
The PlantUML extension is already installed! Just:
1. Open any `.puml` file
2. Press `Alt+D` for preview
3. Edit and see live updates

### Online Rendering
You can also render these diagrams online using:
- [PlantUML Online Server](http://www.plantuml.com/plantuml/uml/)
- [PlantText](https://www.planttext.com/)

### Local Rendering (Advanced)
To render locally, you need:
1. Java runtime
2. PlantUML JAR file
3. Graphviz (for some diagram types)

```bash
# Example command to generate PNG
java -jar plantuml.jar c4-level1-context.puml
```

### C4 PlantUML Library
These diagrams use the C4-PlantUML library which provides C4 model-specific notation. The library is automatically included via the `!include` statements at the top of each file.

## Diagram Overview

### Level 1: System Context
Shows the Cronbach's Alpha Web Application in context with its users and external systems (Redis, MongoDB, ArpY system).

### Level 2: Container
Shows the main containers:
- Vue.js Single Page Application
- FastAPI Server
- Static File Server
- External databases and services

### Level 3: Components
Detailed view of components within each container:
- Frontend: Vue components, routing, services
- Backend: API endpoints, middleware, business logic
- Statistics: Mathematical functions and data processing

### Level 4: Code
Example code-level diagram showing the internal structure of the Cronbach's alpha calculation function.

## Viewing the Diagrams

For the best experience, view the complete C4 model documentation in `../C4_MODEL.md` which includes rendered versions of these diagrams along with detailed explanations.