# Building the Single-File Executable

This guide shows how to build the standalone executable from the single `video_to_audio_converter.py` file.

## File Overview

**Main File:** `video_to_audio_converter.py` - All code in one file (~750 lines)

This single file contains everything needed for the video-to-audio converter, making it much easier to compile with PyInstaller.

## Quick Build (Windows)

### Prerequisites
1. Windows 10/11 (64-bit)
2. Python 3.8+ installed
3. FFmpeg binary downloaded

### Steps

1. **Download FFmpeg**
   ```cmd
   # Visit: https://www.gyan.dev/ffmpeg/builds/
   # Download: ffmpeg-release-essentials.zip
   # Extract ffmpeg.exe to: ffmpeg/windows/ffmpeg.exe
   ```

2. **Install PyInstaller**
   ```cmd
   pip install pyinstaller
   ```

3. **Build the Executable**
   ```cmd
   pyinstaller video_to_audio_single.spec
   ```

4. **Find Your Executable**
   ```cmd
   # Location: dist/video-to-audio.exe
   # Size: ~100-150MB
   ```

## Alternative: One-Line Build Command

If you prefer not to use the .spec file:

```cmd
pyinstaller --onefile ^
  --name video-to-audio ^
  --add-data "ffmpeg/windows/ffmpeg.exe;ffmpeg/windows" ^
  --console ^
  video_to_audio_converter.py
```

## Testing

After building, test the executable:

```cmd
dist\video-to-audio.exe "C:\Path\To\Videos"
```

## File Structure

```
Bulk-Passive-Listening/
├── video_to_audio_converter.py    # Single-file version (all code here)
├── video_to_audio_single.spec     # PyInstaller spec file
├── ffmpeg/
│   └── windows/
│       └── ffmpeg.exe             # Download this (95MB)
└── dist/
    └── video-to-audio.exe         # Built executable (100-150MB)
```

## Advantages of Single-File Version

✅ **Easier to compile** - Just one Python file
✅ **Easier to modify** - All code in one place
✅ **Easier to distribute** - Just share one .py file
✅ **Same functionality** - Identical features to multi-file version

## Running as Python Script

You can also run it directly without compiling:

```cmd
python video_to_audio_converter.py "C:\Path\To\Videos"
```

## Building for Other Platforms

### macOS

```bash
# Download FFmpeg
brew install ffmpeg
mkdir -p ffmpeg/macos
cp $(which ffmpeg) ffmpeg/macos/

# Build
pyinstaller video_to_audio_single.spec
```

### Linux

```bash
# Install FFmpeg
sudo apt-get install ffmpeg

# Build
pyinstaller video_to_audio_single.spec
```

## Troubleshooting

### "FFmpeg binary not found"
- Ensure `ffmpeg.exe` is in `ffmpeg/windows/ffmpeg.exe`
- Check the path is correct

### Executable is too large
- This is normal - FFmpeg is ~95MB
- Total size of 100-150MB is expected

### Import errors during build
- Make sure you're building from the repo root directory
- Ensure PyInstaller is up to date: `pip install --upgrade pyinstaller`

## Distribution

The built executable is fully standalone:
- ✅ No Python installation required
- ✅ No FFmpeg installation required
- ✅ No dependencies needed
- ✅ Just download and run!

Perfect for sharing with users who don't want to install anything.

---

**Recommended:** Use `video_to_audio_converter.py` + `video_to_audio_single.spec` for the easiest build experience.
