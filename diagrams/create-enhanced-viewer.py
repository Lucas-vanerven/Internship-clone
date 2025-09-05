#!/usr/bin/env python3
"""
Enhanced HTML viewer generator for C4 diagrams including multi-level views
"""

import os
from pathlib import Path

def create_enhanced_html_viewer(output_dir, puml_files):
    """Create an enhanced HTML file to view all generated diagrams with better organization"""
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>C4 Model Diagrams - Cronbach's Alpha Web App</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0; padding: 20px; background: #f5f5f5; line-height: 1.6;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 { color: #333; text-align: center; margin-bottom: 10px; }
        .subtitle { text-align: center; color: #666; margin-bottom: 30px; }
        
        .section { margin: 40px 0; }
        .section h2 { 
            color: #2c3e50; border-bottom: 3px solid #3498db; 
            padding-bottom: 10px; margin-bottom: 20px;
        }
        
        .diagram-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(600px, 1fr)); gap: 20px; }
        .diagram { 
            background: white; padding: 20px; border-radius: 8px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); transition: transform 0.2s;
        }
        .diagram:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(0,0,0,0.15); }
        .diagram h3 { color: #34495e; margin-top: 0; }
        .diagram img { max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; }
        .level { background: #e3f2fd; padding: 5px 10px; border-radius: 4px; font-size: 0.9em; display: inline-block; margin-bottom: 10px; }
        .combined { background: #f3e5f5; }
        .overview { background: #e8f5e8; }
        
        .description { color: #555; margin: 10px 0; font-style: italic; }
        .features { background: #f8f9fa; padding: 15px; border-radius: 4px; margin: 10px 0; }
        .features ul { margin: 5px 0; padding-left: 20px; }
        .features li { margin: 5px 0; }
        
        .navigation { position: sticky; top: 20px; background: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        .nav-links { display: flex; gap: 15px; flex-wrap: wrap; }
        .nav-links a { text-decoration: none; color: #3498db; padding: 5px 10px; border-radius: 4px; }
        .nav-links a:hover { background: #e3f2fd; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏗️ C4 Model Architecture Diagrams</h1>
        <p class="subtitle"><strong>Cronbach's Alpha Web Application</strong> - Complete Architecture Documentation</p>
        
        <div class="navigation">
            <strong>Quick Navigation:</strong>
            <div class="nav-links">
                <a href="#combined">🔄 Combined Views</a>
                <a href="#individual">📊 Individual Levels</a>
                <a href="#context">🌍 Context</a>
                <a href="#container">📦 Containers</a>
                <a href="#components">⚙️ Components</a>
                <a href="#code">💻 Code</a>
            </div>
        </div>
"""
    
    # Combined/Multi-level diagrams section
    html_content += """
        <div class="section" id="combined">
            <h2>🔄 Multi-Level Combined Views</h2>
            <p>These diagrams show multiple C4 levels in a single view, providing comprehensive architecture overviews.</p>
            <div class="diagram-grid">
"""
    
    combined_diagrams = {
        'c4-all-levels-combined': {
            'title': 'All Levels Combined',
            'description': 'Complete system view showing context, containers, and key components in one integrated diagram',
            'features': [
                'System context with external actors',
                'Container boundaries and relationships', 
                'Key components within each container',
                'Data flow across all levels'
            ]
        },
        'c4-hierarchical-all-levels': {
            'title': 'Hierarchical Multi-Level View',
            'description': 'Structured presentation showing clear separation between C4 levels',
            'features': [
                'Clear level separation with color coding',
                'Top-down hierarchical layout',
                'Explicit level relationships',
                'Code structure examples'
            ]
        },
        'c4-integrated-overview': {
            'title': 'Integrated System Overview', 
            'description': 'Compact integration showing the complete system with all major components',
            'features': [
                'Nested container boundaries',
                'Detailed component interactions',
                'External system integrations',
                'Comprehensive data flow'
            ]
        }
    }
    
    for name, info in combined_diagrams.items():
        if any(f.stem == name for f in puml_files):
            html_content += f"""
                <div class="diagram">
                    <h3>{info['title']}</h3>
                    <span class="level combined">Multi-Level View</span>
                    <p class="description">{info['description']}</p>
                    <div class="features">
                        <strong>Key Features:</strong>
                        <ul>
                            {''.join(f'<li>{feature}</li>' for feature in info['features'])}
                        </ul>
                    </div>
                    <img src="{name}.png" alt="{info['title']}" />
                </div>
"""
    
    html_content += """
            </div>
        </div>
        
        <div class="section" id="individual">
            <h2>📊 Individual Level Diagrams</h2>
            <p>Traditional C4 model diagrams showing each level separately with detailed focus.</p>
            <div class="diagram-grid">
"""
    
    # Individual level diagrams
    individual_diagrams = {
        'c4-level1-context': {
            'level': 'Level 1: System Context',
            'title': 'System Context',
            'description': 'Shows how the Cronbach\'s Alpha application fits into the broader ecosystem with users and external systems',
            'focus': 'External perspective and system boundaries'
        },
        'c4-level2-container': {
            'level': 'Level 2: Container',
            'title': 'Container Architecture',
            'description': 'High-level technology choices showing Vue.js frontend, FastAPI backend, and data storage systems',
            'focus': 'Technology stack and container relationships'
        },
        'c4-level3-frontend-components': {
            'level': 'Level 3: Components',
            'title': 'Frontend Components',
            'description': 'Vue.js single-page application component structure with routing and user interface elements',
            'focus': 'Frontend component organization'
        },
        'c4-level3-backend-components': {
            'level': 'Level 3: Components', 
            'title': 'Backend Components',
            'description': 'FastAPI server components handling API endpoints, business logic, and data processing',
            'focus': 'Backend service architecture'
        },
        'c4-level3-statistics-components': {
            'level': 'Level 3: Components',
            'title': 'Statistics Engine',
            'description': 'Core statistical calculation components for Cronbach\'s alpha analysis and data processing',
            'focus': 'Statistical computation logic'
        },
        'c4-level4-code-example': {
            'level': 'Level 4: Code',
            'title': 'Code Structure',
            'description': 'Internal implementation details of the Cronbach\'s alpha calculation function',
            'focus': 'Code-level implementation'
        }
    }
    
    for name, info in individual_diagrams.items():
        if any(f.stem == name for f in puml_files):
            level_class = 'level'
            if 'Level 4' in info['level']:
                level_class += ' overview'
            
            html_content += f"""
                <div class="diagram">
                    <h3>{info['title']}</h3>
                    <span class="{level_class}">{info['level']}</span>
                    <p class="description">{info['description']}</p>
                    <div class="features">
                        <strong>Focus:</strong> {info['focus']}
                    </div>
                    <img src="{name}.png" alt="{info['title']}" />
                </div>
"""
    
    html_content += """
            </div>
        </div>
        
        <div class="section">
            <h2>📖 About C4 Model</h2>
            <div style="background: white; padding: 20px; border-radius: 8px;">
                <p>The C4 model is a lean graphical notation technique for modeling software architecture. It consists of four hierarchical levels:</p>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin: 20px 0;">
                    <div style="background: #e3f2fd; padding: 15px; border-radius: 4px;">
                        <strong>Level 1: System Context</strong><br>
                        Shows how the software system fits into the world around it
                    </div>
                    <div style="background: #f3e5f5; padding: 15px; border-radius: 4px;">
                        <strong>Level 2: Container</strong><br>
                        Shows the high-level technology choices and responsibilities
                    </div>
                    <div style="background: #e8f5e8; padding: 15px; border-radius: 4px;">
                        <strong>Level 3: Component</strong><br>
                        Shows how containers are made up of components
                    </div>
                    <div style="background: #fff3e0; padding: 15px; border-radius: 4px;">
                        <strong>Level 4: Code</strong><br>
                        Shows how components are implemented (optional)
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    viewer_file = output_dir / "index.html"
    with open(viewer_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"📄 Enhanced HTML viewer created: {viewer_file}")

def main():
    """Update the HTML viewer with enhanced multi-level diagram support"""
    
    diagrams_dir = Path(__file__).parent
    output_dir = diagrams_dir / "generated-png"
    
    if not output_dir.exists():
        print("❌ PNG output directory not found. Run generate-png-diagrams.py first.")
        return
    
    # Find all .puml files
    puml_files = list(diagrams_dir.glob("*.puml"))
    
    print("🎨 Creating enhanced HTML viewer for multi-level diagrams...")
    create_enhanced_html_viewer(output_dir, puml_files)
    print("✅ Enhanced viewer ready!")

if __name__ == "__main__":
    main()
