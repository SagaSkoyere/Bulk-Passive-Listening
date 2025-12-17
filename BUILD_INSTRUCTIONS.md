# Build Instructions

This document provides detailed instructions for building the standalone executable for different platforms.

## Building for Windows

### Prerequisites

1. **Windows Machine** (or Windows VM)
2. **Python 3.8+** installed
3. **Git** (optional, for cloning the repository)

### Step-by-Step Instructions

#### 1. Get the Source Code

```cmd
git clone https://github.com/yourusername/Bulk-Passive-Listening.git
cd Bulk-Passive-Listening
```

Or download and extract the ZIP from GitHub.

#### 2. Download FFmpeg for Windows

1. Visit: https://www.gyan.dev/ffmpeg/builds/
2. Download: **ffmpeg-release-essentials.zip** (or the latest release)
3. Extract the ZIP file
4. Copy `ffmpeg.exe` from the `bin` folder to `ffmpeg/windows/` in the project
   ```
   Bulk-Passive-Listening/
   └── ffmpeg/
       └── windows/
           └── ffmpeg.exe   <-- Place it here
   ```

#### 3. Install PyInstaller

```cmd
pip install pyinstaller
```

Or install all dev dependencies:

```cmd
pip install -r requirements-dev.txt
```

#### 4. Build the Executable

```cmd
pyinstaller video_to_audio.spec
```

This will take a few minutes. You'll see lots of output as PyInstaller analyzes dependencies and bundles everything together.

#### 5. Find Your Executable

The built executable will be at:

```
dist/video-to-audio.exe
```

File size should be approximately **100-150 MB** (most of it is the ffmpeg binary).

#### 6. Test the Executable

```cmd
dist\video-to-audio.exe
```

Try it with a folder of test videos to ensure it works correctly.

#### 7. Distribute

The `video-to-audio.exe` file is completely standalone. You can:
- Copy it anywhere
- Send it to users
- Upload it as a GitHub release

Users do NOT need Python, FFmpeg, or any other dependencies installed.

---

## Building for macOS

### Prerequisites

1. **macOS Machine** (10.13 or later)
2. **Python 3.8+** installed
3. **Homebrew** (recommended)

### Step-by-Step Instructions

#### 1. Get the Source Code

```bash
git clone https://github.com/yourusername/Bulk-Passive-Listening.git
cd Bulk-Passive-Listening
```

#### 2. Download FFmpeg for macOS

Option A - Using Homebrew (easiest):
```bash
brew install ffmpeg
cp $(which ffmpeg) ffmpeg/macos/ffmpeg
chmod +x ffmpeg/macos/ffmpeg
```

Option B - Manual Download:
1. Visit: https://evermeet.cx/ffmpeg/
2. Download the latest `ffmpeg` binary
3. Extract and copy to `ffmpeg/macos/ffmpeg`
4. Make it executable: `chmod +x ffmpeg/macos/ffmpeg`

#### 3. Install PyInstaller

```bash
pip3 install pyinstaller
```

#### 4. Build the Executable

```bash
pyinstaller video_to_audio.spec
```

#### 5. Find Your Executable

The built executable will be at:

```
dist/video-to-audio
```

#### 6. Test the Executable

```bash
./dist/video-to-audio
```

#### 7. Code Signing (Optional but Recommended)

macOS may prevent unsigned applications from running. You can:

**Option A - Sign it (requires Apple Developer account):**
```bash
codesign --force --deep --sign "Your Developer ID" dist/video-to-audio
```

**Option B - Users bypass Gatekeeper:**
- Right-click the app → Open
- Click "Open" when warned about unidentified developer

---

## Building for Linux

### Prerequisites

1. **Linux Machine** (Ubuntu, Debian, Fedora, etc.)
2. **Python 3.8+** installed
3. **FFmpeg** installed

### Step-by-Step Instructions

#### 1. Get the Source Code

```bash
git clone https://github.com/yourusername/Bulk-Passive-Listening.git
cd Bulk-Passive-Listening
```

#### 2. Install FFmpeg

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch
sudo pacman -S ffmpeg
```

The Linux build typically uses system FFmpeg rather than bundling it.

#### 3. Install PyInstaller

```bash
pip3 install pyinstaller
```

#### 4. Build the Executable

```bash
pyinstaller video_to_audio.spec
```

#### 5. Find Your Executable

```
dist/video-to-audio
```

#### 6. Test the Executable

```bash
./dist/video-to-audio
```

**Note**: On Linux, the executable may still require FFmpeg to be installed on the target system.

---

## Troubleshooting Build Issues

### "Module not found" errors during build
- Make sure all source files are in the `video_to_audio/` directory
- Run PyInstaller from the project root directory

### FFmpeg binary not found in executable
- Verify FFmpeg is in the correct location (`ffmpeg/windows/ffmpeg.exe` for Windows)
- Check the PyInstaller output for warnings about missing files
- Ensure `video_to_audio.spec` includes the correct binaries section

### Executable is too large
- This is normal. FFmpeg is ~80-100MB by itself
- The total executable size of 100-150MB is expected
- Consider using UPX compression (enabled in the spec file)

### Antivirus flags the executable
- This is a common false positive with PyInstaller executables
- Submit the file to your antivirus vendor as a false positive
- Users may need to create an exception

### "Permission denied" on Linux/macOS
- Make the executable file executable: `chmod +x dist/video-to-audio`

---

## Clean Build

If you need to rebuild from scratch:

```bash
# Remove previous build artifacts
rm -rf build/ dist/

# Rebuild
pyinstaller video_to_audio.spec
```

On Windows:
```cmd
rmdir /s /q build dist
pyinstaller video_to_audio.spec
```

---

## Advanced: Customizing the Build

### Add a Custom Icon (Windows)

1. Create or download a `.ico` file (256x256 recommended)
2. Place it in the project root (e.g., `icon.ico`)
3. Edit `video_to_audio.spec`:
   ```python
   exe = EXE(
       ...
       icon='icon.ico',  # Add this line
   )
   ```

### Change Executable Name

Edit `video_to_audio.spec`:
```python
exe = EXE(
    ...
    name='MyCustomName',  # Change from 'video-to-audio'
)
```

### Reduce Executable Size

Edit `video_to_audio.spec`:
```python
exe = EXE(
    ...
    upx=True,              # Enable UPX compression
    upx_exclude=['ffmpeg.exe'],  # Don't compress ffmpeg (already optimized)
)
```

---

## Creating GitHub Releases

After building the executable:

1. **Create a release on GitHub**:
   - Go to Releases → Draft a new release
   - Tag version: `v1.0.0`
   - Title: `Video to Audio Converter v1.0.0`

2. **Upload the executable**:
   - Attach `video-to-audio.exe` (Windows)
   - Attach `video-to-audio` (macOS/Linux)
   - Include SHA256 checksums for security

3. **Write release notes**:
   - List new features
   - List bug fixes
   - Include usage instructions link

Example:
```
## Video to Audio Converter v1.0.0

### Download
- [Windows (64-bit)](video-to-audio.exe) - 145 MB
- [macOS (Intel/Apple Silicon)](video-to-audio-macos) - 120 MB

### Features
- Batch convert video files to audio
- Remove silence
- Normalize audio levels
- Multi-track support

See [README.md](README.md) for full usage instructions.
```

---

## Build Checklist

Before releasing:

- [ ] Test executable on clean Windows machine (no Python installed)
- [ ] Test with various video formats (.mp4, .mov, .avi, .mkv, etc.)
- [ ] Test all three options combinations
- [ ] Test error handling (corrupted files, missing tracks)
- [ ] Test with paths containing spaces and special characters
- [ ] Verify file size is reasonable (~100-150MB)
- [ ] Run virus scan on executable
- [ ] Create checksums (SHA256)
- [ ] Write release notes
- [ ] Update version number in code

---

## Platform-Specific Notes

### Windows
- Users on Windows 10/11 may see SmartScreen warning on first run
- Executable should work on any 64-bit Windows without dependencies

### macOS
- Users need to right-click → Open on first run due to Gatekeeper
- Consider code signing for better user experience
- May need to build separate binaries for Intel vs Apple Silicon

### Linux
- Linux users are comfortable with dependencies
- Consider documenting system FFmpeg requirement instead of bundling

---

## Getting Help

If you encounter build issues:
1. Check PyInstaller documentation: https://pyinstaller.org/
2. Verify FFmpeg is in the correct location
3. Open an issue on GitHub with:
   - Your platform (Windows/macOS/Linux)
   - Python version
   - Full error message
   - PyInstaller version
