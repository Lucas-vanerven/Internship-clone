#!/usr/bin/env python3
"""
Extract PlantUML diagrams from C4_MODEL.md and update .puml files
"""

import re
import os
from pathlib import Path

def extract_plantuml_from_markdown(md_file):
    """Extract PlantUML code blocks from markdown file"""
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all PlantUML code blocks
    pattern = r'```plantuml\n(.*?)\n```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    diagrams = []
    for match in matches:
        # Extract the diagram name from @startuml line
        first_line = match.split('\n')[0]
        if '@startuml' in first_line:
            diagram_name = first_line.replace('@startuml', '').strip()
            if not diagram_name:
                diagram_name = "unnamed"
            diagrams.append((diagram_name, match))
    
    return diagrams

def update_puml_files(diagrams, output_dir):
    """Update or create .puml files from extracted diagrams"""
    
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    print(f"📁 Updating PlantUML files in: {output_dir}")
    
    for diagram_name, content in diagrams:
        # Map diagram names to file names
        file_mapping = {
            'C4_Context': 'c4-level1-context.puml',
            'C4_Container': 'c4-level2-container.puml',
            'C4_Component_Frontend': 'c4-level3-frontend-components.puml',
            'C4_Component_Backend': 'c4-level3-backend-components.puml',
            'C4_Component_Statistics': 'c4-level3-statistics-components.puml',
            'C4_Code': 'c4-level4-code-example.puml'
        }
        
        filename = file_mapping.get(diagram_name, f"{diagram_name.lower()}.puml")
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated: {filename}")

def main():
    """Main function"""
    
    print("📄 Extracting PlantUML diagrams from C4_MODEL.md...")
    
    # Paths
    project_root = Path(__file__).parent.parent
    md_file = project_root / "C4_MODEL.md"
    diagrams_dir = Path(__file__).parent
    
    if not md_file.exists():
        print(f"❌ File not found: {md_file}")
        return
    
    # Extract diagrams
    diagrams = extract_plantuml_from_markdown(md_file)
    
    if not diagrams:
        print("❌ No PlantUML diagrams found in C4_MODEL.md")
        return
    
    print(f"📊 Found {len(diagrams)} PlantUML diagrams:")
    for name, _ in diagrams:
        print(f"  - {name}")
    
    print()
    
    # Update .puml files
    update_puml_files(diagrams, diagrams_dir)
    
    print()
    print("🎉 Successfully extracted and updated PlantUML files!")
    print("💡 You can now:")
    print("   - Use VS Code PlantUML extension to preview diagrams")
    print("   - Run generate-png-diagrams.py to create PNG images")
    print("   - Run generate-ascii-diagrams.py to create ASCII art")

if __name__ == "__main__":
    main()
