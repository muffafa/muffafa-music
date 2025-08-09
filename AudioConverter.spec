# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Import required modules for Windows compatibility
import sys
import os
from PyInstaller.utils.hooks import collect_all

# Collect all pydub dependencies
pydub_datas, pydub_binaries, pydub_hiddenimports = collect_all('pydub')

a = Analysis(
    ['modern_app.py'],
    pathex=[],
    binaries=pydub_binaries,
    datas=pydub_datas,
    hiddenimports=[
        'pydub',
        'pydub.audio_segment',
        'pydub.effects',
        'pydub.silence',
        'pydub.utils',
        'pytubefix',
        'ssl',
        'threading',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'audioop',  # Required for pydub audio processing
        'wave',     # Audio file format support
        'array',    # Array operations for audio
        'struct',   # Binary data handling
        'math',     # Mathematical operations
        'os',       # Operating system interface
        'subprocess',  # For FFmpeg integration
        'platform',  # Platform detection
        'tempfile',  # Temporary file handling
        'shutil',    # File operations
        'io',        # Input/output operations
        'logging',   # Logging support
    ] + pydub_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AudioConverter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

# Create macOS app bundle
app = BUNDLE(
    exe,
    name='AudioConverter.app',
    icon=None,
    bundle_identifier='com.muffafa.audioconverter',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'CFBundleDisplayName': 'Modern Audio Converter',
        'CFBundleExecutableType': 'APPL',
        'NSAppleScriptEnabled': False,
    }
)