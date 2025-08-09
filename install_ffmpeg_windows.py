#!/usr/bin/env python3
"""
Automated FFmpeg Installer for Windows
Downloads and installs FFmpeg for the Modern Audio Converter application.
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil
from pathlib import Path
import winreg

def add_to_path(directory):
    """Add directory to Windows PATH environment variable"""
    try:
        # Open the registry key for environment variables
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                           "Environment", 
                           0, 
                           winreg.KEY_ALL_ACCESS)
        
        # Get current PATH value
        try:
            current_path, _ = winreg.QueryValueEx(key, "PATH")
        except FileNotFoundError:
            current_path = ""
        
        # Check if directory is already in PATH
        if directory.lower() in current_path.lower():
            print(f"✅ {directory} is already in PATH")
            winreg.CloseKey(key)
            return True
        
        # Add directory to PATH
        new_path = f"{current_path};{directory}" if current_path else directory
        winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
        winreg.CloseKey(key)
        
        print(f"✅ Added {directory} to PATH")
        return True
        
    except Exception as e:
        print(f"❌ Failed to add to PATH: {e}")
        return False

def download_file(url, filename):
    """Download file with progress indicator"""
    def progress_hook(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percent = min(100, (downloaded * 100) // total_size)
            print(f"\rDownloading... {percent}%", end="", flush=True)
    
    try:
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, filename, progress_hook)
        print(f"\n✅ Downloaded {filename}")
        return True
    except Exception as e:
        print(f"\n❌ Failed to download {filename}: {e}")
        return False

def extract_zip(zip_path, extract_to):
    """Extract ZIP file"""
    try:
        print(f"Extracting {zip_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"✅ Extracted to {extract_to}")
        return True
    except Exception as e:
        print(f"❌ Failed to extract {zip_path}: {e}")
        return False

def check_ffmpeg_installed():
    """Check if FFmpeg is already installed and working"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        if result.returncode == 0:
            print("✅ FFmpeg is already installed and working!")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        pass
    
    return False

def install_ffmpeg():
    """Main FFmpeg installation function"""
    print("🎵 FFmpeg Installer for Modern Audio Converter")
    print("=" * 60)
    
    # Check if already installed
    if check_ffmpeg_installed():
        return True
    
    # Define paths and URLs
    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    download_path = Path("ffmpeg-release-essentials.zip")
    install_dir = Path("C:/ffmpeg")
    bin_dir = install_dir / "bin"
    
    print(f"Installing FFmpeg to: {install_dir}")
    
    # Create installation directory
    try:
        install_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {install_dir}")
    except Exception as e:
        print(f"❌ Failed to create directory {install_dir}: {e}")
        return False
    
    # Download FFmpeg
    if not download_file(ffmpeg_url, download_path):
        return False
    
    # Extract FFmpeg
    temp_extract = Path("temp_ffmpeg")
    if not extract_zip(download_path, temp_extract):
        return False
    
    # Find the extracted FFmpeg folder (it has a version number in the name)
    extracted_folders = list(temp_extract.glob("ffmpeg-*"))
    if not extracted_folders:
        print("❌ Could not find extracted FFmpeg folder")
        return False
    
    ffmpeg_folder = extracted_folders[0]
    
    # Copy files to installation directory
    try:
        print("Copying FFmpeg files...")
        
        # Copy bin directory
        src_bin = ffmpeg_folder / "bin"
        if src_bin.exists():
            if bin_dir.exists():
                shutil.rmtree(bin_dir)
            shutil.copytree(src_bin, bin_dir)
            print(f"✅ Copied bin directory to {bin_dir}")
        
        # Copy other directories if they exist
        for dir_name in ["doc", "presets"]:
            src_dir = ffmpeg_folder / dir_name
            dst_dir = install_dir / dir_name
            if src_dir.exists():
                if dst_dir.exists():
                    shutil.rmtree(dst_dir)
                shutil.copytree(src_dir, dst_dir)
                print(f"✅ Copied {dir_name} directory")
        
    except Exception as e:
        print(f"❌ Failed to copy FFmpeg files: {e}")
        return False
    
    # Add to PATH
    if not add_to_path(str(bin_dir)):
        print("⚠️  Could not automatically add FFmpeg to PATH")
        print(f"   Please manually add {bin_dir} to your PATH environment variable")
    
    # Cleanup
    try:
        download_path.unlink()
        shutil.rmtree(temp_extract)
        print("✅ Cleaned up temporary files")
    except Exception as e:
        print(f"⚠️  Could not clean up temporary files: {e}")
    
    # Verify installation
    print("\n🔍 Verifying FFmpeg installation...")
    
    # Note: PATH changes require a new process to take effect
    ffmpeg_exe = bin_dir / "ffmpeg.exe"
    if ffmpeg_exe.exists():
        try:
            result = subprocess.run([str(ffmpeg_exe), '-version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            if result.returncode == 0:
                print("✅ FFmpeg installation successful!")
                print("\n📋 IMPORTANT: You may need to restart your command prompt")
                print("   or IDE for PATH changes to take effect.")
                return True
        except Exception as e:
            print(f"⚠️  FFmpeg installed but verification failed: {e}")
    
    print("❌ FFmpeg installation may have failed")
    return False

def main():
    """Main function"""
    if sys.platform != "win32":
        print("❌ This installer is only for Windows")
        return False
    
    try:
        success = install_ffmpeg()
        if success:
            print("\n🎉 FFmpeg installation completed!")
            print("\n📋 Next steps:")
            print("   1. Restart your command prompt or IDE")
            print("   2. Test with: ffmpeg -version")
            print("   3. Run: python modern_app.py")
        else:
            print("\n❌ FFmpeg installation failed")
            print("\n📋 Manual installation:")
            print("   1. Download from: https://www.gyan.dev/ffmpeg/builds/")
            print("   2. Extract to C:\\ffmpeg")
            print("   3. Add C:\\ffmpeg\\bin to PATH")
        
        return success
        
    except KeyboardInterrupt:
        print("\n⚠️  Installation cancelled by user")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to continue...")
    sys.exit(0 if success else 1)
