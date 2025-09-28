#!/bin/bash
# Tavo Scanner Binary Build Script

set -e

echo "🔨 Building Tavo Scanner Binary..."

# Check if we're in the right directory
if [ ! -f "packages/scanner/tavo_scanner.py" ]; then
    echo "❌ Error: Must be run from tavo-api root directory"
    exit 1
fi

# Detect OS for cross-platform compatibility
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    IS_WINDOWS=true
    PYTHON_CMD="python"
    VENV_ACTIVATE="build-venv/Scripts/activate"
    BINARY_EXT=".exe"
else
    IS_WINDOWS=false
    PYTHON_CMD="python3"
    VENV_ACTIVATE="build-venv/bin/activate"
    BINARY_EXT=""
fi

# Activate build virtual environment
if [ ! -d "build-venv" ]; then
    echo "📦 Creating build virtual environment..."
    $PYTHON_CMD -m venv build-venv
fi

echo "🐍 Activating build environment..."
source $VENV_ACTIVATE

# Install dependencies
echo "📥 Installing build dependencies..."
pip install pyinstaller PyYAML

# Download engines
echo "⬇️  Downloading scanner engines..."
cd packages/scanner
chmod +x download_engines.sh
./download_engines.sh
cd ../..

# Build the binary
echo "🏗️  Building binary..."
cd packages/scanner

# Clean previous builds
rm -rf build dist

# Set data separator based on OS (colon for Unix, semicolon for Windows)
if [ "$IS_WINDOWS" = true ]; then
    DATA_SEP=";"
else
    DATA_SEP=":"
fi

# Build with PyInstaller
pyinstaller --onefile --hidden-import yaml --add-data "engines${DATA_SEP}engines" --name tavo-scanner tavo_scanner.py

echo "✅ Build complete!"
echo "📁 Binary location: packages/scanner/dist/tavo-scanner$BINARY_EXT"
echo "📏 Binary size: $(ls -lh "dist/tavo-scanner$BINARY_EXT" | awk '{print $5}')"

# Test the binary
echo "🧪 Testing binary..."
if ./dist/tavo-scanner$BINARY_EXT --help > /dev/null 2>&1; then
    echo "✅ Binary test passed!"
else
    echo "❌ Binary test failed!"
    exit 1
fi

echo "🎉 Tavo Scanner binary is ready for distribution!"