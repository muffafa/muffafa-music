# 🪟 Windows Installation Guide - Modern Audio Converter

This guide covers both **building the installer** (for developers) and **installing the app** (for end users) on Windows.

---

## 📦 For End Users: Installing the App

### System Requirements
- Windows 10 or later (Windows 11 recommended)
- No Python installation required
- FFmpeg (automatically handled by the installer)

### Installation Steps

1. **Download the Installer**
   - Download `AudioConverterInstaller.exe` from the releases page
   - File size: ~12-15MB

2. **Run the Installer**
   - Double-click `AudioConverterInstaller.exe`
   - If Windows SmartScreen appears, click "More info" → "Run anyway"
   - The installer will guide you through the setup process

3. **Installation Process**
   - **Welcome Screen**: Click "Next"
   - **License Agreement**: Read and accept the license terms
   - **Installation Directory**: Choose install location (default: `C:\Program Files\Muffafa\Modern Audio Converter\`)
   - **Start Menu Folder**: Choose Start Menu folder name
   - **Additional Tasks**: Select desktop shortcut option
   - **Installation**: Click "Install" and wait for completion

4. **Launch the Application**
   - **Option A**: Double-click desktop shortcut (if created)
   - **Option B**: Start Menu → "Modern Audio Converter"
   - **Option C**: Windows Search → type "Audio Converter"
   - **Option D**: Run from installation directory

### ✅ What You Get
- Clean GUI application (no command prompt windows)
- Start Menu integration
- Desktop shortcut (optional)
- Add/Remove Programs entry
- Windows taskbar integration
- Native Windows look and feel

### 🔄 Updating
- Download and run the new installer
- It will automatically update the existing installation
- Your settings and preferences will be preserved

### 🗑️ Uninstalling
- **Method 1**: Settings → Apps → "Modern Audio Converter" → Uninstall
- **Method 2**: Control Panel → Programs → "Modern Audio Converter" → Uninstall
- **Method 3**: Start Menu → "Modern Audio Converter" → "Uninstall"

---

## 🛠️ For Developers: Building the Installer

### Prerequisites
- Windows 10 or later
- Python 3.7+ ([Download from python.org](https://www.python.org/downloads/))
- NSIS (Nullsoft Scriptable Install System) - [Download here](https://nsis.sourceforge.io/)
- Git for Windows (optional but recommended)

### Development Setup

1. **Install Python**
   - Download from [python.org](https://www.python.org/downloads/)
   - **Important**: Check "Add Python to PATH" during installation
   - Verify installation: `python --version`

2. **Install NSIS**
   - Download from [nsis.sourceforge.io](https://nsis.sourceforge.io/)
   - Install with default settings
   - Verify installation: `makensis /VERSION`

3. **Clone the Repository**
   ```cmd
   git clone <repository-url>
   cd muffafa-music
   ```

4. **Create Virtual Environment**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

5. **Install Dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

6. **Test the Application**
   ```cmd
   python modern_app.py
   ```

### Building the Installer

#### Method 1: Automated (Recommended)
```cmd
# Activate virtual environment first
venv\Scripts\activate

# This handles everything automatically
python build_installers.py
```

#### Method 2: Manual Steps
```cmd
# Step 1: Activate virtual environment
venv\Scripts\activate

# Step 2: Build the executable
pyinstaller AudioConverter.spec

# Step 3: Create the installer
makensis installer_windows.nsi
```

#### Method 3: Using Build Script
```cmd
# If you have make installed (via chocolatey or similar)
make install-and-build
```

### 📁 Output Files
After successful build:
- **Executable**: `dist\AudioConverter.exe`
- **Installer**: `AudioConverterInstaller.exe` (in project root)

### 🔧 Customizing the Build

#### Changing App Icon
1. Create a `.ico` file (256x256 recommended)
2. Update `installer_windows.nsi`:
   ```nsis
   !define MUI_ICON "path\to\your\icon.ico"
   !define MUI_UNICON "path\to\your\icon.ico"
   ```

#### Modifying Installer Properties
Edit `installer_windows.nsi`:
```nsis
!define APPNAME "Your App Name"
!define COMPANYNAME "Your Company"
!define DESCRIPTION "Your app description"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0
```

#### Adding/Removing Shortcuts
In `installer_windows.nsi`, modify the installation section:
```nsis
# Desktop shortcut (optional)
CreateShortcut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\AudioConverter.exe"

# Start menu shortcuts
CreateDirectory "$SMPROGRAMS\${COMPANYNAME}"
CreateShortcut "$SMPROGRAMS\${COMPANYNAME}\${APPNAME}.lnk" "$INSTDIR\AudioConverter.exe"
```

### 🐛 Troubleshooting

#### Python Issues
- **"python is not recognized"**: Add Python to PATH or reinstall with PATH option
- **Virtual environment issues**: Use full path: `C:\path\to\project\venv\Scripts\activate`
- **Permission errors**: Run Command Prompt as Administrator

#### PyInstaller Issues
- **"pyinstaller is not recognized"**: Ensure virtual environment is activated
- **Missing modules**: Add to `hiddenimports` in `AudioConverter.spec`
- **Large executable size**: Use `--exclude-module` for unused packages

#### NSIS Issues
- **"makensis is not recognized"**: Add NSIS to PATH or use full path
- **Compilation errors**: Check syntax in `installer_windows.nsi`
- **File not found errors**: Ensure `dist\AudioConverter.exe` exists before running NSIS

#### Installer Issues
- **SmartScreen warnings**: Sign the installer with a code signing certificate
- **Antivirus false positives**: Submit to antivirus vendors for whitelisting
- **Installation fails**: Run installer as Administrator

### 📋 Distribution Checklist

Before distributing your installer:
- [ ] Test on clean Windows system without Python
- [ ] Verify installer creates proper shortcuts
- [ ] Test application launches without command prompt
- [ ] Verify all features work (audio conversion, YouTube download)
- [ ] Test uninstallation removes all files
- [ ] Check Add/Remove Programs entry is correct
- [ ] Scan with Windows Defender and other antivirus tools

### 🔐 Code Signing (Recommended)
For professional distribution:
1. Purchase code signing certificate from trusted CA
2. Install certificate in Windows Certificate Store
3. Sign the installer:
   ```cmd
   signtool sign /a /t http://timestamp.digicert.com AudioConverterInstaller.exe
   ```

### 📊 File Sizes
- Executable: ~12-15MB
- Installer: ~12-15MB
- Installed size: ~20-25MB
- Dependencies included: pydub, pytubefix, tkinter, Python runtime

### 🚀 Advanced Options

#### Creating MSI Installer
For enterprise deployment, consider creating an MSI:
1. Install WiX Toolset
2. Create WiX configuration files
3. Build MSI package

#### Portable Version
To create a portable version:
1. Copy `dist\AudioConverter.exe` to desired location
2. Include all dependencies in same folder
3. No installation required

#### Auto-Updater
Consider implementing auto-update functionality:
1. Check for updates on startup
2. Download and install updates automatically
3. Notify users of available updates

---

## 🆘 Support

### Common Issues
- **FFmpeg not found**: The installer should handle this automatically
- **YouTube download fails**: Check internet connection and firewall settings
- **Audio conversion errors**: Verify input file formats are supported
- **Antivirus warnings**: Add application to antivirus exclusions

### Performance Tips
- Close other applications during large batch conversions
- Use SSD storage for better performance
- Ensure adequate free disk space for conversions

### Getting Help
- Check the main README.md for general usage
- Review error messages in the app's status bar
- Check Windows Event Viewer for system-level errors
- For development issues, check the build logs

### System Integration
The installer automatically:
- Registers file associations (optional)
- Creates uninstaller entry
- Sets up Start Menu shortcuts
- Configures Windows Firewall exceptions (if needed)

---

**Made with ❤️ for Windows users**
