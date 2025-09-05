#!/usr/bin/env python3
"""
PlantUML PNG Generator for C4 Model Diagrams
Generates PNG images from PlantUML files using the online PlantUML server
"""

import os
import requests
import zlib
import base64
from pathlib import Path

def encode_plantuml(source):
    """Encode PlantUML source for URL transmission using PlantUML's deflate method"""
    # Use deflate compression (not gzip/zlib wrapper)
    import zlib
    
    # Convert to bytes
    source_bytes = source.encode('utf-8')
    
    # Compress using deflate (raw deflate, not zlib format)
    compressed = zlib.compress(source_bytes)[2:-4]  # Remove zlib header and trailer
    
    # Use PlantUML's base64 variant (URL-safe with custom alphabet)
    plantuml_alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    standard_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    
    # First encode with standard base64
    encoded = base64.b64encode(compressed).decode('ascii')
    
    # Translate to PlantUML alphabet
    translation_table = str.maketrans(standard_alphabet, plantuml_alphabet)
    plantuml_encoded = encoded.translate(translation_table)
    
    return plantuml_encoded

def generate_png_from_puml(puml_file, output_dir):
    """Generate PNG from a PlantUML file using online server"""
    
    # Read the PlantUML source
    with open(puml_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encode for PlantUML server
    encoded = encode_plantuml(content)
    
    # Generate PNG using PlantUML server
    url = f"http://www.plantuml.com/plantuml/png/{encoded}"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save PNG file
        output_file = output_dir / f"{puml_file.stem}.png"
        with open(output_file, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Generated: {output_file.name}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to generate {puml_file.name}: {e}")
        return False

def main():
    """Main function to generate all PNG diagrams"""
    
    print("🎨 Generating C4 Model PNG Diagrams...")
    
    # Setup directories
    diagrams_dir = Path(__file__).parent
    output_dir = diagrams_dir / "generated-png"
    output_dir.mkdir(exist_ok=True)
    
    print(f"📁 Input directory: {diagrams_dir}")
    print(f"📁 Output directory: {output_dir}")
    
    # Find all .puml files
    puml_files = list(diagrams_dir.glob("*.puml"))
    
    if not puml_files:
        print("❌ No PlantUML files found!")
        return
    
    print(f"📊 Found {len(puml_files)} PlantUML files")
    print()
    
    # Generate PNG for each file
    success_count = 0
    for puml_file in sorted(puml_files):
        if generate_png_from_puml(puml_file, output_dir):
            success_count += 1
    
    print()
    print(f"🎉 Successfully generated {success_count}/{len(puml_files)} PNG diagrams")
    print(f"📁 Images saved to: {output_dir}")
    
    # Create an HTML viewer
    create_html_viewer(output_dir, puml_files)

def create_html_viewer(output_dir, puml_files):
    """Create an HTML file to view all generated diagrams"""
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>C4 Model Diagrams - Cronbach's Alpha Web App</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0; padding: 20px; background: #f5f5f5;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #333; text-align: center; }
        .diagram { 
            background: white; margin: 20px 0; padding: 20px; 
            border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .diagram h2 { color: #555; margin-top: 0; }
        .diagram img { max-width: 100%; height: auto; border: 1px solid #ddd; }
        .level { background: #e3f2fd; padding: 5px 10px; border-radius: 4px; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏗️ C4 Model Diagrams</h1>
        <p><strong>Cronbach's Alpha Web Application</strong> - Architecture Documentation</p>
"""
    
    diagram_info = {
        'c4-level1-context': ('Level 1: System Context', 'Shows how the application fits into the broader ecosystem'),
        'c4-level2-container': ('Level 2: Container', 'Shows the high-level technology containers and their relationships'),
        'c4-level3-frontend-components': ('Level 3: Frontend Components', 'Shows the Vue.js frontend component structure'),
        'c4-level3-backend-components': ('Level 3: Backend Components', 'Shows the FastAPI backend component structure'),
        'c4-level3-statistics-components': ('Level 3: Statistics Components', 'Shows the statistical calculation components'),
        'c4-level4-code-example': ('Level 4: Code', 'Shows the internal structure of the Cronbach\'s alpha function')
    }
    
    for puml_file in sorted(puml_files):
        name = puml_file.stem
        if name in diagram_info:
            title, description = diagram_info[name]
            level = title.split(':')[0]
            
            html_content += f"""
        <div class="diagram">
            <h2>{title}</h2>
            <span class="level">{level}</span>
            <p>{description}</p>
            <img src="{name}.png" alt="{title}" />
        </div>
"""
    
    html_content += """
    </div>
</body>
</html>
"""
    
    viewer_file = output_dir / "index.html"
    with open(viewer_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"📄 HTML viewer created: {viewer_file}")

if __name__ == "__main__":
    main()
