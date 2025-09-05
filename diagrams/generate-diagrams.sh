#!/bin/bash

# C4 Model Diagram Generator Script
# This script generates PNG images from PlantUML files using the online PlantUML server

set -e

DIAGRAMS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$DIAGRAMS_DIR/generated"

echo "🏗️  Generating C4 Model Diagrams"
echo "Input directory: $DIAGRAMS_DIR"
echo "Output directory: $OUTPUT_DIR"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Function to generate diagram from PlantUML file
generate_diagram() {
    local puml_file="$1"
    local base_name=$(basename "$puml_file" .puml)
    local output_file="$OUTPUT_DIR/${base_name}.png"
    
    echo "📊 Generating $base_name..."
    
    # Use curl to send the PlantUML content to the online server
    # The server expects the content to be encoded, but for simplicity we'll use the text endpoint
    curl -s -X POST \
        -H "Content-Type: text/plain" \
        --data-binary "@$puml_file" \
        "http://www.plantuml.com/plantuml/png/" \
        -o "$output_file"
    
    if [ $? -eq 0 ]; then
        echo "✅ Generated: $output_file"
    else
        echo "❌ Failed to generate: $output_file"
    fi
}

# Check if curl is available
if ! command -v curl &> /dev/null; then
    echo "❌ curl is required but not installed. Please install curl and try again."
    exit 1
fi

echo ""
echo "🚀 Starting diagram generation..."

# Generate all PlantUML diagrams
for puml_file in "$DIAGRAMS_DIR"/*.puml; do
    if [ -f "$puml_file" ]; then
        generate_diagram "$puml_file"
    fi
done

echo ""
echo "✨ Diagram generation complete!"
echo "📁 Generated files are in: $OUTPUT_DIR"
echo ""
echo "🔍 To view the diagrams:"
echo "   - Open the PNG files in any image viewer"
echo "   - Or view the complete documentation in ../C4_MODEL.md"