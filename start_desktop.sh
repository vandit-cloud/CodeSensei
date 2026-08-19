#!/bin/bash
# CodeSensei Desktop App - Quick Start Script

echo "🥋 CodeSensei Desktop App Setup"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.8 or higher from python.org"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed!"
    echo "Please install pip"
    exit 1
fi

echo "📦 Installing dependencies..."
pip3 install -r requirements_desktop.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "🚀 Starting CodeSensei Desktop App..."
python3 desktop_app.py
