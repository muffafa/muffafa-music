#!/usr/bin/env python3
"""
Environment Setup and Verification Script for Modern Audio Converter
Helps users set up the correct Python environment and dependencies.
"""

import sys
import subprocess
import os
import platform
from pathlib import Path

def run_command(cmd, capture_output=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def check_python_version():
    """Check if current Python version is compatible"""
    current = sys.version_info
    print(f"Current Python: {current.major}.{current.minor}.{current.micro}")
    
    if current >= (3, 13):
        print("❌ Python 3.13+ detected - audioop module is not available!")
        return False
    elif current < (3, 7):
        print("❌ Python version too old!")
        return False
    else:
        print("✅ Python version is compatible")
        return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    
    requirements = [
        "pydub>=0.25.1",
        "pytubefix>=6.0.0",
        "pyinstaller>=5.0.0",
        "requests>=2.25.0"
    ]
    
    for req in requirements:
        print(f"Installing {req}...")
        success, stdout, stderr = run_command(f"{sys.executable} -m pip install {req}")
        if success:
            print(f"✅ {req} installed successfully")
        else:
            print(f"❌ Failed to install {req}: {stderr}")
            return False
    
    return True

def check_ffmpeg():
    """Check if FFmpeg is available"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print("✅ FFmpeg is available")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        pass
    
    print("❌ FFmpeg is NOT available")
    print("   Audio conversion will not work without FFmpeg")
    if platform.system() == "Windows":
        print("   Run: python install_ffmpeg_windows.py")
    else:
        print("   Install FFmpeg using your package manager")
    return False

def verify_modules():
    """Verify that all required modules can be imported"""
    print("\n🔍 Verifying module imports...")
    
    modules_to_test = [
        ("tkinter", "GUI framework"),
        ("pydub", "Audio processing"),
        ("pytubefix", "YouTube downloading"),
        ("audioop", "Audio operations (may use fallback)"),
        ("subprocess", "System commands"),
        ("threading", "Multi-threading"),
        ("json", "JSON handling"),
        ("os", "Operating system interface"),
        ("sys", "System interface")
    ]
    
    all_good = True
    for module, description in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError as e:
            if module == "audioop":
                print(f"⚠️  {module} - {description} (will use fallback)")
            else:
                print(f"❌ {module} - {description} - ERROR: {e}")
                all_good = False
    
    return all_good

def create_virtual_environment():
    """Create a virtual environment with correct Python version"""
    print("\n🐍 Setting up virtual environment...")
    
    venv_path = Path("venv")
    if venv_path.exists():
        print("Virtual environment already exists")
        return True
    
    success, stdout, stderr = run_command(f"{sys.executable} -m venv venv")
    if success:
        print("✅ Virtual environment created successfully")
        
        # Determine activation script based on OS
        if platform.system() == "Windows":
            activate_script = "venv\\Scripts\\activate.bat"
            pip_path = "venv\\Scripts\\pip"
        else:
            activate_script = "source venv/bin/activate"
            pip_path = "venv/bin/pip"
        
        print(f"\n📋 To activate the virtual environment:")
        print(f"   {activate_script}")
        print(f"\n📋 To install dependencies in the virtual environment:")
        print(f"   {pip_path} install -r requirements.txt")
        
        return True
    else:
        print(f"❌ Failed to create virtual environment: {stderr}")
        return False

def main():
    """Main setup function"""
    print("🎵 Modern Audio Converter - Environment Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        print("\n❌ SETUP FAILED: Incompatible Python version")
        print("\n📋 Recommended actions:")
        print("   1. Install Python 3.9.21 from: https://www.python.org/downloads/release/python-3921/")
        print("   2. Create a virtual environment with the correct version")
        print("   3. Run this script again")
        return False
    
    # Check FFmpeg
    ffmpeg_ok = check_ffmpeg()
    
    # Verify modules
    if not verify_modules():
        print("\n📦 Some modules are missing. Installing dependencies...")
        if not install_dependencies():
            print("\n❌ SETUP FAILED: Could not install dependencies")
            return False
    
    # Final verification
    if ffmpeg_ok:
        print("\n🎉 Environment setup completed successfully!")
    else:
        print("\n⚠️  Environment setup completed with warnings!")
        print("   FFmpeg is missing - audio conversion will not work")
    
    print("\n📋 Next steps:")
    if not ffmpeg_ok and platform.system() == "Windows":
        print("   1. Run: python install_ffmpeg_windows.py")
        print("   2. Run: python check_python_version.py")
        print("   3. Run: python modern_app.py")
    else:
        print("   1. Run: python check_python_version.py")
        print("   2. Run: python modern_app.py")
        print("   3. For building installer: make windows-installer")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
