# 🍎 macOS Installation Guide - Modern Audio Converter

This guide covers both **building the installer** (for developers) and **installing the app** (for end users) on macOS.

---

## 📦 For End Users: Installing the App

### System Requirements
- macOS 10.14 (Mojave) or later
- No Python installation required
- FFmpeg (will be prompted if needed)

### Installation Steps

1. **Download the Installer**
   - Download `AudioConverter-Installer.dmg` from the releases page
   - File size: ~10MB

2. **Open the DMG File**
   - Double-click `AudioConverter-Installer.dmg`
   - A new window will open showing the installer contents

3. **Install the Application**
   - Drag `AudioConverter.app` to the `Applications` folder
   - Wait for the copy process to complete
   - Eject the DMG by clicking the eject button in Finder

4. **Launch the Application**
   - **Option A**: Open Applications folder and double-click `AudioConverter.app`
   - **Option B**: Press `Cmd + Space`, type "Audio Converter", press Enter
   - **Option C**: Find it in Launchpad

5. **First Launch (Security)**
   - If you see "AudioConverter can't be opened because it's from an unidentified developer":
     - Right-click on `AudioConverter.app` in Applications
     - Select "Open" from the context menu
     - Click "Open" in the security dialog
     - This only needs to be done once

### ✅ What You Get
- Clean GUI application (no terminal windows)
- Dock integration with proper icon
- Spotlight search integration
- Native macOS look and feel
- Proper window management and notifications

### 🗑️ Uninstalling
- Simply drag `AudioConverter.app` from Applications to Trash
- Empty the Trash to complete removal

---

## 🛠️ For Developers: Building the Installer

### Prerequisites
- macOS 10.14 or later
- Python 3.7+
- Xcode Command Line Tools: `xcode-select --install`

### Development Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd muffafa-music
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test the Application**
   ```bash
   python modern_app.py
   ```

### Building the Installer

#### Method 1: Automated (Recommended)
```bash
# This handles everything automatically
python build_installers.py
```

#### Method 2: Manual Steps
```bash
# Step 1: Build the app bundle
pyinstaller AudioConverter.spec

# Step 2: Create the DMG installer
./create_macos_installer.sh
```

#### Method 3: Using Makefile
```bash
# Install dependencies and build installer
make install-and-build
```

### 📁 Output Files
After successful build:
- **App Bundle**: `dist/AudioConverter.app`
- **DMG Installer**: `dist/AudioConverter-Installer.dmg`

### 🔧 Customizing the Build

#### Changing App Icon
1. Create an `.icns` file (1024x1024 recommended)
2. Update `AudioConverter.spec`:
   ```python
   icon='path/to/your/icon.icns'
   ```

#### Modifying App Bundle Info
Edit the `info_plist` section in `AudioConverter.spec`:
```python
info_plist={
    'NSHighResolutionCapable': 'True',
    'CFBundleDisplayName': 'Your App Name',
    'CFBundleVersion': '1.0.0',
    'CFBundleShortVersionString': '1.0.0',
    # Add more properties as needed
}
```

#### Customizing DMG Appearance
Edit `create_macos_installer.sh`:
- Change DMG name: `DMG_NAME="YourAppName-Installer"`
- Add background image: `BACKGROUND_IMAGE="your_background.png"`
- Modify README content

### 🐛 Troubleshooting

#### Build Issues
- **"command not found: pyinstaller"**: Ensure virtual environment is activated
- **Missing modules**: Add to `hiddenimports` in `AudioConverter.spec`
- **Permission denied**: Run `chmod +x create_macos_installer.sh`

#### App Bundle Issues
- **App won't launch**: Check Console.app for error messages
- **Missing dependencies**: Verify all modules are included in spec file
- **Terminal window appears**: Ensure `console=False` in spec file

#### DMG Creation Issues
- **"hdiutil: create failed"**: Check available disk space
- **Permission errors**: Ensure write permissions in project directory

### 📋 Distribution Checklist

Before distributing your DMG:
- [ ] Test on clean macOS system without Python
- [ ] Verify app launches without terminal windows
- [ ] Test all features (audio conversion, YouTube download)
- [ ] Check app appears correctly in Applications folder
- [ ] Verify Spotlight search finds the app
- [ ] Test uninstallation process

### 🔐 Code Signing (Optional)
For distribution outside the App Store:
1. Get Apple Developer account
2. Create certificates in Keychain Access
3. Update `codesign_identity` in `AudioConverter.spec`
4. Sign the DMG: `codesign -s "Your Identity" AudioConverter-Installer.dmg`

### 📊 File Sizes
- App Bundle: ~10MB
- DMG Installer: ~10MB
- Dependencies included: pydub, pytubefix, tkinter, Python runtime

---

## 🆘 Support

### Common Issues
- **FFmpeg not found**: Install via Homebrew: `brew install ffmpeg`
- **YouTube download fails**: Check internet connection and URL validity
- **Audio conversion errors**: Verify input file formats are supported

### Getting Help
- Check the main README.md for general usage
- Review error messages in the app's status bar
- For development issues, check the build logs

---

**Made with ❤️ for macOS users**
