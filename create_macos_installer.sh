#!/bin/bash
# Modern Audio Converter - macOS Installer Creation Script
# Creates a professional .dmg installer for macOS

set -e

# Configuration
APP_NAME="Modern Audio Converter"
APP_BUNDLE="AudioConverter.app"
DMG_NAME="AudioConverter-Installer"
VERSION="1.0.0"
BACKGROUND_IMAGE="installer_background.png"  # Optional background image

echo "🍎 Creating macOS Installer for ${APP_NAME}"
echo "================================================"

# Check if app bundle exists
if [ ! -d "dist/${APP_BUNDLE}" ]; then
    echo "❌ Error: ${APP_BUNDLE} not found in dist/ directory"
    echo "Please build the app bundle first using PyInstaller"
    exit 1
fi

# Create temporary directory for DMG contents
TEMP_DIR=$(mktemp -d)
DMG_DIR="${TEMP_DIR}/dmg"
mkdir -p "${DMG_DIR}"

echo "📦 Preparing DMG contents..."

# Copy app bundle to DMG directory
cp -R "dist/${APP_BUNDLE}" "${DMG_DIR}/"

# Create Applications symlink for easy installation
ln -s /Applications "${DMG_DIR}/Applications"

# Create a README file for the installer
cat > "${DMG_DIR}/README.txt" << EOF
Modern Audio Converter v${VERSION}

INSTALLATION:
1. Drag "AudioConverter.app" to the "Applications" folder
2. Launch from Applications or Spotlight search
3. Enjoy converting audio files and downloading YouTube videos!

FEATURES:
- Batch convert audio files to MP3
- Download YouTube videos as MP3
- Modern, user-friendly interface
- No terminal windows or command line needed

REQUIREMENTS:
- macOS 10.14 or later
- FFmpeg (will be prompted to install if needed)

SUPPORT:
For issues or questions, please visit our GitHub repository.

© 2024 Muffafa - Modern Audio Converter
EOF

# Set proper permissions
chmod -R 755 "${DMG_DIR}/${APP_BUNDLE}"

echo "🔨 Creating DMG image..."

# Create the DMG
DMG_PATH="dist/${DMG_NAME}.dmg"

# Remove existing DMG if it exists
[ -f "${DMG_PATH}" ] && rm "${DMG_PATH}"

# Create DMG with proper settings
hdiutil create -volname "${APP_NAME}" \
    -srcfolder "${DMG_DIR}" \
    -ov \
    -format UDZO \
    -imagekey zlib-level=9 \
    "${DMG_PATH}"

# Clean up temporary directory
rm -rf "${TEMP_DIR}"

# Get file size
DMG_SIZE=$(du -h "${DMG_PATH}" | cut -f1)

echo "✅ DMG created successfully!"
echo "📁 Location: ${DMG_PATH}"
echo "📏 Size: ${DMG_SIZE}"
echo ""
echo "🎉 macOS installer ready for distribution!"
echo ""
echo "💡 Installation Instructions for Users:"
echo "1. Download and open the .dmg file"
echo "2. Drag 'AudioConverter.app' to Applications folder"
echo "3. Launch from Applications or Spotlight"
echo ""
echo "📋 Distribution Notes:"
echo "- The .dmg file contains everything needed"
echo "- Users don't need Python or dependencies installed"
echo "- App will run without terminal windows"
echo "- Proper macOS integration with dock and spotlight"
