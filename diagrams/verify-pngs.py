#!/usr/bin/env python3
"""
Verify that all generated PNG files are valid
"""

import os
from pathlib import Path

def verify_png_files():
    """Check that PNG files are valid and not empty"""
    
    output_dir = Path(__file__).parent / "generated-png"
    
    if not output_dir.exists():
        print("❌ PNG output directory not found!")
        return
    
    png_files = list(output_dir.glob("*.png"))
    
    if not png_files:
        print("❌ No PNG files found!")
        return
    
    print(f"🔍 Verifying {len(png_files)} PNG files...")
    print()
    
    valid_count = 0
    
    for png_file in sorted(png_files):
        file_size = png_file.stat().st_size
        
        # Check if file exists and has reasonable size (PNG files should be > 1KB)
        if file_size > 1024:
            # Quick check for PNG header
            with open(png_file, 'rb') as f:
                header = f.read(8)
                if header.startswith(b'\x89PNG\r\n\x1a\n'):
                    print(f"✅ {png_file.name} - {file_size:,} bytes - Valid PNG")
                    valid_count += 1
                else:
                    print(f"❌ {png_file.name} - Invalid PNG header")
        else:
            print(f"⚠️  {png_file.name} - {file_size} bytes - File too small")
    
    print()
    print(f"🎉 {valid_count}/{len(png_files)} PNG files are valid!")
    
    if valid_count == len(png_files):
        print("✨ All diagrams generated successfully!")
        print(f"📁 Location: {output_dir}")
        print(f"🌐 HTML Viewer: {output_dir / 'index.html'}")
    else:
        print("⚠️  Some files may need regeneration")

if __name__ == "__main__":
    verify_png_files()
