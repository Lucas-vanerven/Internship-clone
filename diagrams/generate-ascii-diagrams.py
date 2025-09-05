#!/usr/bin/env python3
"""
Simple diagram generator for C4 Model documentation
Creates ASCII art representations of the architectural diagrams
"""

import os

def create_ascii_diagrams():
    """Generate ASCII art representations of the C4 diagrams"""
    
    diagrams_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(diagrams_dir, "ascii-diagrams")
    os.makedirs(output_dir, exist_ok=True)
    
    # Level 1: System Context
    context_diagram = """
┌─────────────────────────────────────────────────────────────────┐
│                    System Context Diagram                       │
└─────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐         ┌─────────────────┐
    │   Researcher/   │◄────────┤ System Admin    │
    │    Analyst      │         │                 │
    └─────────┬───────┘         └─────────────────┘
              │                           │
              │ HTTPS                     │ HTTPS
              ▼                           ▼
    ┌─────────────────────────────────────────────────────────────┐
    │        Cronbach's Alpha Web Application                     │
    │     (Web-based statistical reliability analysis)           │
    └─────────┬─────────┬─────────┬─────────┬─────────────────────┘
              │         │         │         │
              │         │         │         │
              ▼         ▼         ▼         ▼
    ┌─────────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────┐
    │File System  │ │  Redis  │ │ MongoDB │ │ArpY Data    │
    │             │ │  Cache  │ │Database │ │System       │
    └─────────────┘ └─────────┘ └─────────┘ └─────────────┘
"""

    # Level 2: Container
    container_diagram = """
┌─────────────────────────────────────────────────────────────────┐
│                    Container Diagram                            │
└─────────────────────────────────────────────────────────────────┘

                        ┌─────────────┐
                        │    User     │
                        │(Researcher) │
                        └──────┬──────┘
                               │ HTTPS
                               ▼
    ┌───────────────────────────────────────────────────────────────┐
    │        Cronbach's Alpha Web Application                       │
    │                                                               │
    │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐│
    │  │     Vue.js      │  │   FastAPI       │  │ Static Files    ││
    │  │  Single Page    │◄─┤   API Server    │◄─┤    Server       ││
    │  │  Application    │  │                 │  │                 ││
    │  └─────────────────┘  └────────┬────────┘  └─────────────────┘│
    └───────────────────────────────┼─────────────────────────────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
    ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
    │  File Storage   │  │  Redis Cache    │  │  MongoDB        │
    │ (Filesystem)    │  │                 │  │  Database       │
    └─────────────────┘  └─────────────────┘  └─────────────────┘
    
                            ┌─────────────────┐
                            │  ArpY Module    │
                            │ (Python Pkg)    │
                            └─────────────────┘
"""

    # Level 3: Frontend Components
    frontend_components = """
┌─────────────────────────────────────────────────────────────────┐
│              Frontend Components (Vue.js SPA)                   │
└─────────────────────────────────────────────────────────────────┘

                        ┌─────────────────┐
                        │   Vue Router    │
                        │                 │
                        └────────┬────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
                ▼                ▼                ▼
    ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
    │  Upload Page    │ │Factor Calculator│ │   Home Page     │
    │                 │ │                 │ │                 │
    └─────────┬───────┘ └─────────┬───────┘ └─────────────────┘
              │                   │
              │ ┌─────────────────┘
              │ │         ┌─────────────────┐
              │ │         │ Database        │
              │ │         │ Combiner Page   │
              │ │         └─────────┬───────┘
              │ │                   │
              └─┼───────────────────┘
                │
                ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                   API Service                               │
    │         (Centralized HTTP client)                          │
    └─────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
          ┌─────────────────────┐
          │   FastAPI Backend   │
          └─────────────────────┘

    Additional Components:
    • Vue Draggable (drag-and-drop functionality)
    • Bootstrap UI (styling and responsive design)
"""

    # Level 3: Backend Components
    backend_components = """
┌─────────────────────────────────────────────────────────────────┐
│              Backend Components (FastAPI)                       │
└─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │                FastAPI Application                          │
    │                                                             │
    │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
    │  │    CORS     │  │ Static File │  │  Jinja2 Templates  │  │
    │  │ Middleware  │  │ Middleware  │  │                     │  │
    │  └─────────────┘  └─────────────┘  └─────────────────────┘  │
    │                                                             │
    │  ┌─────────────────────────────────────────────────────────┐ │
    │  │               API Router (/api)                         │ │
    │  │                                                         │ │
    │  │ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ │ │
    │  │ │File Upload  │ │Factor Group │ │  Calculation        │ │ │
    │  │ │ Handler     │ │ Endpoints   │ │  Endpoints          │ │ │
    │  │ └─────────────┘ └─────────────┘ └─────────────────────┘ │ │
    │  └─────────────────────────────────────────────────────────┘ │
    └─────────────┬─────────────┬─────────────┬─────────────────────┘
                  │             │             │
                  ▼             ▼             ▼
      ┌─────────────────┐ ┌─────────────┐ ┌─────────────────┐
      │Upload Functions │ │Score        │ │  Data Fetcher   │
      │                 │ │Calculator   │ │  (ArpY)         │
      └─────────────────┘ └─────────────┘ └─────────────────┘
"""

    # Level 4: Code Example
    code_diagram = """
┌─────────────────────────────────────────────────────────────────┐
│           Code Level: Cronbach's Alpha Function                 │
└─────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────┐
                    │  pandas.DataFrame   │
                    │   (Input Data)      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Input Validation   │
                    │ • Check ≥2 columns  │
                    │ • Check data rows   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Variance Calculation│
                    │ • Item variances    │
                    │ • Total variance    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Alpha Formula     │
                    │ α = k/(k-1) *       │
                    │   (1 - Σσ²ᵢ/σ²ₜ)   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Result Rounding    │
                    │ Round to 3 decimals │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Return Float      │
                    │ (Cronbach's Alpha)  │
                    └─────────────────────┘

    Dependencies: NumPy (statistical calculations)
    Error Handling: ValueError for invalid inputs
"""

    # Write all diagrams to files
    diagrams = {
        "level1-context.txt": context_diagram,
        "level2-container.txt": container_diagram,
        "level3-frontend-components.txt": frontend_components,
        "level3-backend-components.txt": backend_components,
        "level4-code-example.txt": code_diagram
    }
    
    print("🎨 Generating ASCII C4 Diagrams...")
    
    for filename, content in diagrams.items():
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f"✅ Generated: {filename}")
    
    # Create an index file
    index_content = """
C4 Model ASCII Diagrams
======================

This directory contains ASCII art representations of the C4 model diagrams.

Files:
------
• level1-context.txt - System Context Diagram
• level2-container.txt - Container Diagram  
• level3-frontend-components.txt - Frontend Components
• level3-backend-components.txt - Backend Components
• level4-code-example.txt - Code Level Example

These diagrams provide a text-based view of the system architecture
that can be viewed in any text editor or terminal.

For the complete documentation with detailed explanations,
see ../C4_MODEL.md
"""
    
    with open(os.path.join(output_dir, "README.txt"), 'w') as f:
        f.write(index_content.strip())
    
    print(f"📁 All diagrams saved to: {output_dir}")
    print("🔍 View the README.txt file for an overview")

if __name__ == "__main__":
    create_ascii_diagrams()