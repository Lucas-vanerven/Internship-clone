#!/usr/bin/env python3
"""
Reliable PlantUML PNG Generator using multiple methods
"""

import os
import requests
import tempfile
import subprocess
from pathlib import Path

def method1_online_server_post(puml_file, output_dir):
    """Method 1: Use PlantUML server with POST request"""
    try:
        with open(puml_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Use the POST endpoint which is more reliable
        url = "http://www.plantuml.com/plantuml/png/"
        
        response = requests.post(
            url,
            data={'text': content},
            timeout=30,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        if response.status_code == 200 and response.headers.get('content-type', '').startswith('image/png'):
            output_file = output_dir / f"{puml_file.stem}.png"
            with open(output_file, 'wb') as f:
                f.write(response.content)
            return True, f"✅ Generated: {output_file.name}"
        else:
            return False, f"❌ Server error: {response.status_code}"
            
    except Exception as e:
        return False, f"❌ POST method failed: {e}"

def method2_kroki_server(puml_file, output_dir):
    """Method 2: Use Kroki server as alternative"""
    try:
        with open(puml_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        url = "https://kroki.io/plantuml/png"
        
        response = requests.post(
            url,
            data=content.encode('utf-8'),
            timeout=30,
            headers={'Content-Type': 'text/plain'}
        )
        
        if response.status_code == 200:
            output_file = output_dir / f"{puml_file.stem}.png"
            with open(output_file, 'wb') as f:
                f.write(response.content)
            return True, f"✅ Generated: {output_file.name} (via Kroki)"
        else:
            return False, f"❌ Kroki error: {response.status_code}"
            
    except Exception as e:
        return False, f"❌ Kroki method failed: {e}"

def method3_simple_text_post(puml_file, output_dir):
    """Method 3: Simple text POST to PlantUML"""
    try:
        with open(puml_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try the simple text endpoint
        url = "http://www.plantuml.com/plantuml/png"
        
        response = requests.post(
            url,
            data=content,
            timeout=30,
            headers={'Content-Type': 'text/plain; charset=utf-8'}
        )
        
        if response.status_code == 200 and len(response.content) > 1000:  # PNG files are typically large
            output_file = output_dir / f"{puml_file.stem}.png"
            with open(output_file, 'wb') as f:
                f.write(response.content)
            return True, f"✅ Generated: {output_file.name} (simple POST)"
        else:
            return False, f"❌ Simple POST failed: {response.status_code}"
            
    except Exception as e:
        return False, f"❌ Simple POST method failed: {e}"

def generate_png_with_fallback(puml_file, output_dir):
    """Try multiple methods to generate PNG"""
    
    methods = [
        ("PlantUML POST", method1_online_server_post),
        ("Simple Text POST", method3_simple_text_post),
        ("Kroki Server", method2_kroki_server),
    ]
    
    for method_name, method_func in methods:
        print(f"🔄 Trying {method_name} for {puml_file.name}...")
        success, message = method_func(puml_file, output_dir)
        if success:
            print(f"   {message}")
            return True
        else:
            print(f"   {message}")
    
    print(f"❌ All methods failed for {puml_file.name}")
    return False

def create_fallback_info_file(puml_file, output_dir):
    """Create an info file explaining how to generate the PNG manually"""
    
    info_content = f"""# {puml_file.stem}.png Generation Failed

The automatic PNG generation failed for this diagram. Here are alternative methods:

## Method 1: VS Code PlantUML Extension
1. Open the file: {puml_file.name}
2. Press Alt+D to preview
3. Right-click on preview → "Export Current Diagram"
4. Choose PNG format

## Method 2: Online PlantUML Editor
1. Go to: http://www.plantuml.com/plantuml/uml/
2. Copy and paste the content from: {puml_file.name}
3. Click "Submit" to generate the diagram
4. Right-click on the image → "Save image as..."

## Method 3: PlantText (Alternative)
1. Go to: https://www.planttext.com/
2. Paste the PlantUML code
3. Generate and download the PNG

## File Location
- Source file: {puml_file.absolute()}
- Expected PNG: {output_dir / f"{puml_file.stem}.png"}

## PlantUML Content
```
{open(puml_file, 'r', encoding='utf-8').read()}
```
"""
    
    info_file = output_dir / f"{puml_file.stem}_generation_info.md"
    with open(info_file, 'w', encoding='utf-8') as f:
        f.write(info_content)
    
    print(f"📝 Created generation info: {info_file.name}")

def main():
    """Main function with improved error handling"""
    
    print("🎨 Generating C4 Model PNG Diagrams (Reliable Method)...")
    
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
    failed_files = []
    
    for puml_file in sorted(puml_files):
        print(f"🔨 Processing: {puml_file.name}")
        
        if generate_png_with_fallback(puml_file, output_dir):
            success_count += 1
        else:
            failed_files.append(puml_file)
            create_fallback_info_file(puml_file, output_dir)
        
        print()
    
    print(f"🎉 Successfully generated {success_count}/{len(puml_files)} PNG diagrams")
    
    if failed_files:
        print(f"⚠️  Failed files: {', '.join(f.name for f in failed_files)}")
        print("💡 Check the generated *_generation_info.md files for manual generation instructions")
    
    print(f"📁 Images saved to: {output_dir}")
    
    # Create HTML viewer (if available)
    try:
        import sys
        sys.path.append(str(diagrams_dir))
        from create_enhanced_viewer import create_enhanced_html_viewer
        create_enhanced_html_viewer(output_dir, puml_files)
    except ImportError:
        print("💡 Run create-enhanced-viewer.py separately to create the HTML viewer")

if __name__ == "__main__":
    main()
