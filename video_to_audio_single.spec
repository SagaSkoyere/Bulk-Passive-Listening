# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Video to Audio Converter (Single File Version).

This creates a standalone executable from the single video_to_audio_converter.py file
with bundled ffmpeg binary.

To build:
    pyinstaller video_to_audio_single.spec

Output will be in dist/video-to-audio.exe (Windows) or dist/video-to-audio (macOS/Linux)
"""

import sys
from pathlib import Path

block_cipher = None

# Determine platform-specific ffmpeg binaries to bundle
ffmpeg_binaries = []

if sys.platform == 'win32':
    # Windows: Bundle ffmpeg.exe
    ffmpeg_binaries = [
        ('ffmpeg/windows/ffmpeg.exe', 'ffmpeg/windows'),
    ]
elif sys.platform == 'darwin':
    # macOS: Bundle ffmpeg binary
    ffmpeg_binaries = [
        ('ffmpeg/macos/ffmpeg', 'ffmpeg/macos'),
    ]
elif sys.platform == 'linux':
    # Linux: Bundle ffmpeg binary if available
    # Otherwise, user should have system ffmpeg installed
    linux_ffmpeg = Path('ffmpeg/linux/ffmpeg')
    if linux_ffmpeg.exists():
        ffmpeg_binaries = [
            ('ffmpeg/linux/ffmpeg', 'ffmpeg/linux'),
        ]

a = Analysis(
    ['video_to_audio_converter.py'],
    pathex=[],
    binaries=ffmpeg_binaries,
    datas=[],
    hiddenimports=[],
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
    name='video-to-audio',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compress executable with UPX
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Show console window (required for CLI)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Optional: Add .ico file here for Windows icon
)
