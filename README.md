# 🎵 Modern Audio Converter

A modern desktop audio converter application built with Python and tkinter. Convert audio files to MP3 and download YouTube videos as MP3 files through a beautiful, user-friendly desktop interface with professional installer packages for Windows and macOS.

## ✨ Features

### 📁 Batch Audio Conversion
- Convert multiple audio files to MP3 format
- Supported formats: M4A, MP4, WAV, FLAC, AAC, and more
- Real-time progress tracking with visual feedback
- Automatic file detection and duplicate handling
- Threaded processing for responsive UI

### 📺 YouTube Downloader
- Download YouTube videos as MP3 files
- Video information preview (title, duration, views, channel)
- URL validation with visual feedback
- Progress tracking during download and conversion
- Automatic filename sanitization and duplicate handling

### 🎛️ Modern Desktop Interface
- Clean, modern tkinter interface with custom styling
- Tabbed interface for organized functionality
- Real-time status updates and progress bars
- Responsive design with proper grid layouts
- Error handling with user-friendly messages

### 📦 Professional Distribution
- Native installers for Windows (.exe) and macOS (.dmg)
- No Python installation required for end users
- Proper system integration (Start Menu, Applications folder, dock)
- Professional installation and uninstallation experience
- No terminal windows - pure GUI application

## 🏗️ Project Structure

```
muffafa-music/
├── 🎵 Core Application Files
│   ├── modern_app.py           # Main GUI application
│   ├── audio_converter.py      # Audio conversion logic
│   ├── youtube_downloader.py   # YouTube download logic
│   └── AudioConverter.spec     # PyInstaller configuration
│
├── 📦 Installer Files
│   ├── build_installers.py     # Automated installer builder
│   ├── create_macos_installer.sh # macOS DMG creator
│   └── installer_windows.nsi   # Windows NSIS installer script
│
├── 🔧 Project Configuration
│   ├── requirements.txt        # Python dependencies
│   ├── makefile               # Build automation
│   ├── README.md              # Documentation
│   └── .gitignore             # Git ignore rules
│
└── 📁 Directories
    ├── venv/                  # Virtual environment
    └── music/                 # Output directory for converted files
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7+ (for development)
- FFmpeg (for audio conversion)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd muffafa-music
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python modern_app.py
   ```

## 📦 Creating Installers

### Automated Installer Creation (Recommended)
```bash
# Creates installer for current platform
python build_installers.py
```

### Manual macOS DMG Creation
```bash
# Creates .dmg installer for macOS
./create_macos_installer.sh
```

### Manual Windows Installer Creation
```bash
# On Windows with NSIS installed
makensis installer_windows.nsi
```

### Using Makefile
```bash
# Install dependencies and create installer
make install-and-build
```

Installers will be created in the project directory:
- **macOS**: `AudioConverter-Installer.dmg`
- **Windows**: `AudioConverterInstaller.exe`

## 📦 Dependencies

- **pydub** (≥0.25.1) - Audio processing and conversion
- **pytubefix** (≥6.9.0) - YouTube video downloading (updated pytube fork)
- **pyinstaller** (≥5.0.0) - Creating portable executables
- **tkinter** - GUI framework (included with Python)

## 🎯 Usage

### Audio Conversion
1. Launch the application
2. Go to the "Audio Converter" tab
3. Click "Select Folder" to choose input directory
4. Click "Select Output Folder" for converted files
5. Click "Start Conversion" to begin batch processing

### YouTube Download
1. Go to the "YouTube Downloader" tab
2. Paste a YouTube URL in the input field
3. Click "Get Video Info" to preview
4. Click "Download as MP3" to start download

## 🛠️ Development

### Setting up development environment:
```bash
# Clone and setup
git clone <repository-url>
cd muffafa-music
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run in development mode
python modern_app.py
```

### Building for distribution:
```bash
# Build executable
python build_portable.py

# Or use makefile
make clean  # Clean previous builds
make build  # Build new executable
```

## 🔍 Troubleshooting

### Common Issues:

**FFmpeg not found:**
- Install FFmpeg and ensure it's in your system PATH
- On macOS: `brew install ffmpeg`
- On Windows: Download from https://ffmpeg.org/

**YouTube download fails:**
- Ensure you have the latest pytubefix version
- Check internet connection
- Verify the YouTube URL is valid

**Build fails:**
- Ensure all dependencies are installed
- Try cleaning build directory: `rm -rf build/ dist/`
- Rebuild: `python build_portable.py`

## 📄 License

This project is open source. Please check the license file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions, please open an issue on the repository.

---

**Made with ❤️ using Python and tkinter**
