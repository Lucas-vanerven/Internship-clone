#!/usr/bin/env python3
"""
Alternative PlantUML PNG Generator using local rendering or different servers
"""

import os
import requests
import subprocess
import tempfile
from pathlib import Path

def method_kroki_direct(puml_file, output_dir):
    """Use Kroki.io service which is more reliable"""
    try:
        with open(puml_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Kroki.io endpoint
        url = "https://kroki.io/plantuml/png"
        
        response = requests.post(
            url,
            data=content.encode('utf-8'),
            timeout=60,
            headers={
                'Content-Type': 'text/plain',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        
        if response.status_code == 200 and response.content.startswith(b'\x89PNG'):
            output_file = output_dir / f"{puml_file.stem}.png"
            with open(output_file, 'wb') as f:
                f.write(response.content)
            return True, f"✅ Generated: {output_file.name}"
        else:
            # Check what we actually got
            content_type = response.headers.get('content-type', 'unknown')
            return False, f"❌ Kroki failed: {response.status_code}, Content-Type: {content_type}"
            
    except Exception as e:
        return False, f"❌ Kroki error: {e}"

def method_plantuml_github(puml_file, output_dir):
    """Use alternative PlantUML proxy"""
    try:
        with open(puml_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Alternative server
        url = "https://www.planttext.com/api/plantuml/png"
        
        response = requests.post(
            url,
            data={'text': content},
            timeout=60,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        
        if response.status_code == 200 and response.content.startswith(b'\x89PNG'):
            output_file = output_dir / f"{puml_file.stem}.png"
            with open(output_file, 'wb') as f:
                f.write(response.content)
            return True, f"✅ Generated: {output_file.name} (PlantText)"
        else:
            return False, f"❌ PlantText failed: {response.status_code}"
            
    except Exception as e:
        return False, f"❌ PlantText error: {e}"

def method_local_plantuml(puml_file, output_dir):
    """Try to use local PlantUML if available"""
    try:
        # Check if Java is available
        java_result = subprocess.run(['java', '-version'], 
                                   capture_output=True, text=True, timeout=5)
        
        if java_result.returncode != 0:
            return False, "❌ Java not available for local PlantUML"
        
        # Download PlantUML jar if not present
        plantuml_jar = Path(__file__).parent / "plantuml.jar"
        
        if not plantuml_jar.exists():
            print("📥 Downloading PlantUML jar...")
            jar_url = "https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar"
            response = requests.get(jar_url, timeout=60)
            
            if response.status_code == 200:
                with open(plantuml_jar, 'wb') as f:
                    f.write(response.content)
                print("✅ PlantUML jar downloaded")
            else:
                return False, "❌ Failed to download PlantUML jar"
        
        # Generate PNG using local PlantUML
        output_file = output_dir / f"{puml_file.stem}.png"
        
        cmd = [
            'java', '-jar', str(plantuml_jar),
            '-tpng',
            '-o', str(output_dir),
            str(puml_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and output_file.exists():
            return True, f"✅ Generated: {output_file.name} (Local PlantUML)"
        else:
            return False, f"❌ Local PlantUML failed: {result.stderr}"
            
    except subprocess.TimeoutExpired:
        return False, "❌ Local PlantUML timeout"
    except Exception as e:
        return False, f"❌ Local PlantUML error: {e}"

def generate_png_robust(puml_file, output_dir):
    """Try multiple robust methods"""
    
    methods = [
        ("Kroki.io", method_kroki_direct),
        ("PlantText", method_plantuml_github),
        ("Local PlantUML", method_local_plantuml),
    ]
    
    for method_name, method_func in methods:
        print(f"🔄 Trying {method_name}...")
        success, message = method_func(puml_file, output_dir)
        print(f"   {message}")
        
        if success:
            return True
        
        # Add a small delay between attempts
        import time
        time.sleep(1)
    
    return False

def main():
    """Main function with robust PNG generation"""
    
    print("🚀 Robust PNG Generator for C4 Diagrams")
    print("=" * 50)
    
    diagrams_dir = Path(__file__).parent
    output_dir = diagrams_dir / "generated-png"
    output_dir.mkdir(exist_ok=True)
    
    puml_files = list(diagrams_dir.glob("*.puml"))
    
    if not puml_files:
        print("❌ No PlantUML files found!")
        return
    
    print(f"📊 Processing {len(puml_files)} files...")
    print()
    
    success_count = 0
    
    for i, puml_file in enumerate(sorted(puml_files), 1):
        print(f"[{i}/{len(puml_files)}] 🔨 {puml_file.name}")
        
        if generate_png_robust(puml_file, output_dir):
            success_count += 1
        else:
            print(f"   ❌ All methods failed for {puml_file.name}")
        
        print()
    
    print("=" * 50)
    print(f"🎉 Successfully generated {success_count}/{len(puml_files)} PNG files")
    
    if success_count > 0:
        print(f"📁 Files saved to: {output_dir}")
        
        # Verify the generated files
        print("\n🔍 Verifying generated files...")
        png_files = list(output_dir.glob("*.png"))
        valid_count = 0
        
        for png_file in png_files:
            with open(png_file, 'rb') as f:
                if f.read(8).startswith(b'\x89PNG'):
                    valid_count += 1
                    print(f"   ✅ {png_file.name} - Valid PNG")
                else:
                    print(f"   ❌ {png_file.name} - Invalid")
        
        print(f"\n✨ {valid_count} valid PNG files ready!")
    
    if success_count < len(puml_files):
        print("\n💡 For failed files, you can:")
        print("   1. Use VS Code PlantUML extension (Alt+D to preview)")
        print("   2. Copy content to http://www.plantuml.com/plantuml/uml/")
        print("   3. Use https://kroki.io/ directly")

if __name__ == "__main__":
    main()
