# Build Instructions for Your Setup

## Your FFmpeg Location

The spec files are now configured for your FFmpeg location:
```
C:\Users\spoon\OneDrive\Desktop\SentencioAudioCondense\SentencioAudioCondense\ffmpeg.exe
```

## Quick Build Steps

1. **Open Command Prompt** in the project directory:
   ```
   C:\Users\spoon\OneDrive\Desktop\SentencioAudioCondense\SentencioAudioCondense\
   ```

2. **Install PyInstaller** (if not already installed):
   ```cmd
   pip install pyinstaller
   ```

3. **Build the executable**:
   ```cmd
   pyinstaller video_to_audio_single.spec
   ```

4. **Find your executable**:
   ```
   dist\video-to-audio.exe
   ```

## That's It!

The .exe will be in the `dist` folder and is completely standalone - it includes:
- Python runtime
- All code
- FFmpeg binary

Users can just download and run `video-to-audio.exe` without installing anything.

## File Size

Expect the .exe to be around **100-150 MB** (mostly FFmpeg).

## Testing

After building, test it:
```cmd
dist\video-to-audio.exe "C:\Path\To\Your\Videos"
```

## Troubleshooting

### "FFmpeg binary not found"
- The spec file is configured for your exact path
- Make sure `ffmpeg.exe` exists at:
  `C:\Users\spoon\OneDrive\Desktop\SentencioAudioCondense\SentencioAudioCondense\ffmpeg.exe`

### Build errors
- Make sure you're running the command from the project root
- Try: `pip install --upgrade pyinstaller`

### Antivirus warnings
- This is normal with PyInstaller executables
- Create an exception in your antivirus
- The code is safe - it's all open source

## Distribution

Once built, you can:
- Share `dist\video-to-audio.exe` with anyone
- Upload to GitHub releases
- Email to users
- No installation needed by recipients!

---

**Recommended:** Use `pyinstaller video_to_audio_single.spec` for the easiest build.
