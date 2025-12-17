# Building the Executable

This guide shows how to build the standalone executable from `video_to_audio_converter.py`.

## File Overview

**Main File:** `video_to_audio_converter.py` - All code in one file (~750 lines)

This single file contains everything needed for the video-to-audio converter.

## Quick Build (Windows)

### Prerequisites
1. Windows 10/11 (64-bit)
2. Python 3.8+ installed
3. FFmpeg binary at the configured path

### Steps

1. **Install PyInstaller**
   ```cmd
   pip install pyinstaller
   ```

2. **Build the Executable**
   ```cmd
   pyinstaller video_to_audio.spec
   ```

3. **Find Your Executable**
   ```cmd
   # Location: dist/video-to-audio.exe
   # Size: ~100-150MB
   ```

**Note:** The spec file is pre-configured with the FFmpeg path. No additional setup needed!

## Running Without Building

You can also run the script directly without building:

```cmd
python video_to_audio_converter.py "C:\Path\To\Videos"
```

## Testing

After building, test the executable:

```cmd
dist\video-to-audio.exe "C:\Path\To\Videos"
```

## File Structure

```
Bulk-Passive-Listening/
├── video_to_audio_converter.py    # Main program (all code here)
├── video_to_audio.spec            # PyInstaller build configuration
└── dist/
    └── video-to-audio.exe         # Built executable (100-150MB)
```

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
