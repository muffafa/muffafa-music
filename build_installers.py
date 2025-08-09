#!/usr/bin/env python3
"""
Modern Audio Converter - Cross-Platform Installer Builder
Creates professional installers for both Windows and macOS
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print(f"\n🎵 {title}")
    print("=" * (len(title) + 4))

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)

def build_pyinstaller_app():
    """Build the PyInstaller application"""
    print_header("Building PyInstaller Application")
    
    # Clean previous builds
    print("🧹 Cleaning previous builds...")
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}/")
    
    # Build with PyInstaller
    print("🔨 Building application with PyInstaller...")
    success, output = run_command("pyinstaller AudioConverter.spec")
    
    if success:
        print("✅ PyInstaller build successful!")
        return True
    else:
        print("❌ PyInstaller build failed!")
        print(f"Error: {output}")
        return False

def create_windows_installer():
    """Create Windows installer using NSIS"""
    print_header("Creating Windows Installer")
    
    if platform.system() != "Windows":
        print("⚠️  Windows installer creation requires Windows OS")
        print("💡 To create Windows installer:")
        print("   1. Transfer project to Windows machine")
        print("   2. Install NSIS (https://nsis.sourceforge.io/)")
        print("   3. Run: makensis installer_windows.nsi")
        return False
    
    # Check if NSIS is installed
    success, _ = run_command("makensis /VERSION")
    if not success:
        print("❌ NSIS not found. Please install NSIS first.")
        print("   Download from: https://nsis.sourceforge.io/")
        return False
    
    # Create installer
    print("🔨 Creating Windows installer...")
    success, output = run_command("makensis installer_windows.nsi")
    
    if success:
        print("✅ Windows installer created!")
        print("📁 File: AudioConverterInstaller.exe")
        return True
    else:
        print("❌ Windows installer creation failed!")
        print(f"Error: {output}")
        return False

def create_macos_installer():
    """Create macOS installer (.dmg)"""
    print_header("Creating macOS Installer")
    
    if platform.system() != "Darwin":
        print("⚠️  macOS installer creation requires macOS")
        print("💡 To create macOS installer on other platforms:")
        print("   1. Transfer project to macOS machine")
        print("   2. Run: ./create_macos_installer.sh")
        return False
    
    # Make script executable
    os.chmod("create_macos_installer.sh", 0o755)
    
    # Create DMG installer
    print("🔨 Creating macOS DMG installer...")
    success, output = run_command("./create_macos_installer.sh")
    
    if success:
        print("✅ macOS installer created!")
        print("📁 File: dist/AudioConverter-Installer.dmg")
        return True
    else:
        print("❌ macOS installer creation failed!")
        print(f"Error: {output}")
        return False

def create_license_file():
    """Create a basic license file for the installer"""
    license_content = """MIT License

Copyright (c) 2024 Muffafa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
    
    with open("LICENSE.txt", "w") as f:
        f.write(license_content)
    print("📄 License file created: LICENSE.txt")

def main():
    """Main installer build process"""
    print_header("Modern Audio Converter - Installer Builder")
    
    # Check if we're in the right directory
    if not os.path.exists("modern_app.py"):
        print("❌ Error: modern_app.py not found.")
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    # Create license file
    create_license_file()
    
    # Build the application first
    if not build_pyinstaller_app():
        print("\n❌ Cannot proceed without successful PyInstaller build.")
        sys.exit(1)
    
    # Determine which installers to create based on platform
    current_platform = platform.system()
    
    print(f"\n🖥️  Current platform: {current_platform}")
    
    installers_created = 0
    
    if current_platform == "Darwin":  # macOS
        if create_macos_installer():
            installers_created += 1
        print("\n💡 To create Windows installer:")
        print("   1. Transfer project to Windows machine")
        print("   2. Install NSIS")
        print("   3. Run: python build_installers.py")
        
    elif current_platform == "Windows":
        if create_windows_installer():
            installers_created += 1
        print("\n💡 To create macOS installer:")
        print("   1. Transfer project to macOS machine")
        print("   2. Run: python build_installers.py")
        
    else:  # Linux or other
        print("⚠️  Linux detected. Creating portable executable only.")
        print("💡 For installers:")
        print("   - Windows: Transfer to Windows + install NSIS")
        print("   - macOS: Transfer to macOS")
    
    # Summary
    print_header("Build Summary")
    print(f"✅ PyInstaller build: Success")
    print(f"📦 Installers created: {installers_created}")
    
    if installers_created > 0:
        print("\n🎉 Installer(s) ready for distribution!")
        print("📁 Check the project directory for installer files")
    else:
        print("\n📱 Portable executable available in dist/ directory")
    
    print("\n💡 Distribution Tips:")
    print("- Test installers on clean systems")
    print("- Consider code signing for production")
    print("- Update version numbers for releases")

if __name__ == "__main__":
    main()
