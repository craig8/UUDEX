#!/bin/bash
"""
UUDEX Standalone Client Installation Script

This script installs the UUDEX Standalone CLI and its dependencies.
"""

echo "🚀 Installing UUDEX Standalone CLI..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed. Please install pip3 first."
    exit 1
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Install uudex-api-client
if [ -d "../uudex-api-client" ]; then
    echo "📦 Installing uudex-api-client..."
    pip3 install -e ../uudex-api-client
else
    echo "⚠️  uudex-api-client directory not found. Please ensure it's available."
fi

# Make CLI executable
chmod +x cli.py

echo "✅ Installation complete!"
echo ""
echo "🎉 You can now use the UUDEX Standalone CLI:"
echo "   python cli.py --help"
echo ""
echo "📝 Next steps:"
echo "   1. Set up your certificates in the 'certs' directory"
echo "   2. Run 'python cli.py entities' to verify certificate setup"
echo "   3. Test connection with 'python cli.py status'"
