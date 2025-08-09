#!/usr/bin/env python3
"""
Python Version Compatibility Checker for Modern Audio Converter
Ensures the application runs on a compatible Python version.
"""

import sys
import warnings

# Define compatible Python versions
MIN_PYTHON = (3, 7)
MAX_PYTHON = (3, 12)  # audioop removed in 3.13
RECOMMENDED_PYTHON = (3, 9, 21)

def check_python_version():
    """Check if current Python version is compatible"""
    current_version = sys.version_info
    
    print(f"Current Python version: {current_version.major}.{current_version.minor}.{current_version.micro}")
    print(f"Required: Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ and <= {MAX_PYTHON[0]}.{MAX_PYTHON[1]}")
    print(f"Recommended: Python {RECOMMENDED_PYTHON[0]}.{RECOMMENDED_PYTHON[1]}.{RECOMMENDED_PYTHON[2]}")
    
    # Check minimum version
    if current_version < MIN_PYTHON:
        print(f"❌ ERROR: Python {current_version.major}.{current_version.minor} is too old!")
        print(f"   Please upgrade to Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or newer.")
        return False
    
    # Check maximum version (audioop compatibility)
    if current_version >= (3, 13):
        print(f"⚠️  WARNING: Python {current_version.major}.{current_version.minor} removed the 'audioop' module!")
        print(f"   Audio processing may not work correctly.")
        print(f"   Recommended: Downgrade to Python {RECOMMENDED_PYTHON[0]}.{RECOMMENDED_PYTHON[1]}.{RECOMMENDED_PYTHON[2]}")
        return False
    
    if current_version > MAX_PYTHON:
        print(f"⚠️  WARNING: Python {current_version.major}.{current_version.minor} may have compatibility issues!")
        print(f"   For best compatibility, use Python {RECOMMENDED_PYTHON[0]}.{RECOMMENDED_PYTHON[1]}.{RECOMMENDED_PYTHON[2]}")
        warnings.warn("Using untested Python version", UserWarning)
    
    # Check for recommended version
    if current_version[:3] == RECOMMENDED_PYTHON:
        print(f"✅ Perfect! Using recommended Python version.")
    else:
        print(f"✅ Compatible Python version detected.")
    
    return True

def check_audioop_availability():
    """Check if audioop module is available"""
    try:
        import audioop
        print("✅ audioop module is available")
        return True
    except ImportError:
        print("❌ audioop module is NOT available")
        print("   Using fallback implementation for audio processing")
        return False

if __name__ == "__main__":
    print("🎵 Modern Audio Converter - Python Compatibility Check")
    print("=" * 60)
    
    version_ok = check_python_version()
    audioop_ok = check_audioop_availability()
    
    print("=" * 60)
    
    if version_ok and audioop_ok:
        print("🎉 All checks passed! Your Python environment is fully compatible.")
        sys.exit(0)
    elif version_ok:
        print("⚠️  Python version is compatible, but audioop is missing.")
        print("   The application will use fallback audio processing.")
        sys.exit(0)
    else:
        print("❌ Python version compatibility issues detected!")
        print("\n📋 Recommended actions:")
        print(f"   1. Install Python {RECOMMENDED_PYTHON[0]}.{RECOMMENDED_PYTHON[1]}.{RECOMMENDED_PYTHON[2]}")
        print("   2. Create a virtual environment with the correct version")
        print("   3. Reinstall dependencies in the new environment")
        sys.exit(1)
