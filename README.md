# Video to Audio Converter

A command-line tool that batch-converts video files to audio format (.m4a) for passive listening on your phone or other devices.

## Features

- **Batch Processing**: Convert all video files in a directory at once
- **Multiple Format Support**: Works with .mp4, .mov, .avi, .mkv, .webm, and many more
- **Audio Processing Options**:
  - Remove stretches of silence (below -55dB for >1.2 seconds)
  - Normalize audio levels for comfortable listening (-16 LUFS)
  - Select specific audio track (1, 2, 3, etc.)
- **Error Resilient**: Continues processing all files even if some fail
- **Standalone Executable**: Pre-bundled with Python and FFmpeg - no installation required!

## Quick Start

### For End Users (Windows)

1. **Download** the latest `video-to-audio.exe` from the releases
2. **Double-click** to run, or use from command line:
   ```cmd
   video-to-audio.exe
   ```
3. **Enter** the folder path containing your video files
4. **Answer** the configuration prompts:
   - Remove stretches of silence? (y/n)
   - Normalize audio levels for listening? (y/n)
   - Audio track to use (1/2/3)?
5. **Wait** for processing to complete
6. **Find** your audio files (.m4a) in the same folder as the videos

### Usage Example

```
============================================================
                Video to Audio Converter
============================================================

Enter directory path: C:\Users\YourName\Videos
Directory: C:\Users\YourName\Videos

Configuration Options:
--------------------------------------------------
Remove stretches of silence? (y/n): y
  Use EXPERIMENTAL machine learning for speech detection? (y/n): y
Normalize audio levels for listening? (y/n): y
Audio track to use (1/2/3): 1

Searching for video files...

Found 5 video file(s)

============================================================
Processing Files
============================================================

[1/5] Converting: lecture.mp4
      Output: lecture_audio.m4a
      Status: ✓ Completed

[2/5] Converting: tutorial.mov
      Output: tutorial_audio.m4a
      Status: ✓ Completed

...

============================================================
                        SUMMARY
============================================================
Total files:  5
Successful:   5
Failed:       0

All files converted successfully!
```

## Command-Line Usage

You can also provide the directory path as an argument:

```cmd
video-to-audio.exe "C:\Users\YourName\Videos"
```

## Output Details

- **Format**: AAC audio in .m4a container
- **Bitrate**: 160kbps (good quality for speech and music)
- **Location**: Same folder as the original video files
- **Naming**: Video name + "_audio" suffix (e.g., `video.mp4` → `video_audio.m4a`)
- **Overwrite**: Existing audio files will be overwritten

## Processing Options Explained

### 1. Remove Stretches of Silence

Removes quiet sections from the audio. You'll have two options:

**Traditional Method (FFmpeg):**
- Removes audio below -55dB for more than 1.2 seconds
- Fast and reliable
- Good for general use

**EXPERIMENTAL ML Method (Silero VAD):**
- Uses machine learning for speech detection
- Optimized for anime dialogue and natural speech
- More accurate speech detection with 1-second buffer for natural timing
- Displays detected speech segments with timestamps
- Automatically falls back to traditional method if ML libraries unavailable

Useful for:
- Lectures with long pauses
- Anime episodes with silence
- Recordings with dead air
- Reducing file size and playback time

### 2. Normalize Audio Levels

Adjusts the audio to a consistent loudness level (-16 LUFS), which is optimal for podcasts and speech content. This ensures:
- Comfortable listening volume
- Consistent levels across different files
- No need to adjust volume between tracks

**Note**: Normalization is always applied AFTER silence removal (if both are selected).

### 3. Audio Track Selection

Many video files have multiple audio tracks (e.g., different languages, commentary tracks). Specify which track to extract:
- `1` - First audio track (most common)
- `2` - Second audio track
- `3` - Third audio track, etc.

## Supported Video Formats

.mp4, .mov, .avi, .mkv, .webm, .flv, .wmv, .m4v, .mpg, .mpeg, .3gp, .ogv, .ts, .mts, .m2ts, .vob, .divx, .f4v

## System Requirements

- **Windows**: Windows 10 or later (64-bit)
- **macOS**: macOS 10.13 or later (if macOS version is available)
- **Disk Space**: ~600MB for the executable with ML features (~150MB without ML) + space for output files

**Note**: The executable includes PyTorch and ML libraries for the experimental speech detection feature. All dependencies are bundled - no installation required!

## For Developers

### Prerequisites

- Python 3.8 or later
- FFmpeg binary (automatically downloaded during setup)

### Installation from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Bulk-Passive-Listening.git
   cd Bulk-Passive-Listening
   ```

2. Run directly:
   ```bash
   python video_to_audio_converter.py
   ```

### Building the Executable

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Build:
   ```bash
   pyinstaller video_to_audio.spec
   ```

3. Find your executable:
   ```
   dist/video-to-audio.exe (Windows)
   dist/video-to-audio (macOS/Linux)
   ```

See **BUILD_INSTRUCTIONS.md** for detailed instructions.

### Project Structure

```
video_to_audio_converter.py      # Main program (all code in one file, ~750 lines)
video_to_audio.spec              # PyInstaller build configuration
BUILD_INSTRUCTIONS.md            # Build instructions
BUILD_INSTRUCTIONS_FOR_YOUR_SETUP.md  # Quick build guide
```

All functionality is in the single `video_to_audio_converter.py` file for easy compilation.

### Running Tests

```bash
# Install pytest
pip install pytest

# Run tests
pytest tests/
```

## Technical Details

### FFmpeg Commands

**Basic Conversion:**
```bash
ffmpeg -i input.mp4 -vn -c:a aac -b:a 160k -map 0:a:0 -y output.m4a
```

**Silence Removal:**
```bash
ffmpeg -i input.m4a -af "silenceremove=stop_periods=-1:stop_duration=1.2:stop_threshold=-55dB" -c:a aac -b:a 160k -y output.m4a
```

**Normalization:**
```bash
ffmpeg -i input.m4a -af loudnorm=I=-16:LRA=11:TP=-1.5 -c:a aac -b:a 160k -y output.m4a
```

### Processing Pipeline

When both silence removal and normalization are selected, files are processed in three steps:

1. **Extract Audio**: `video.mp4` → `temp1.m4a` (with selected track)
2. **Remove Silence**: `temp1.m4a` → `temp2.m4a`
3. **Normalize**: `temp2.m4a` → `video.m4a`
4. **Cleanup**: Delete temporary files

## Troubleshooting

### "No video files found in directory"
- Ensure you're pointing to the correct directory
- Check that the directory contains supported video formats
- Try using an absolute path (e.g., `C:\Users\Name\Videos`)

### "FFmpeg binary not found"
- If using the Python version, ensure ffmpeg is in the correct location
- If using the executable, this should never happen (ffmpeg is bundled)

### "Error: Directory not found or not accessible"
- Check the path is correct
- Ensure you have read/write permissions for the directory
- On Windows, use quotes around paths with spaces: `"C:\My Videos"`

### Conversion fails for specific files
- The file may be corrupted
- The file may not have an audio track
- Try a different audio track number (some files use track 2 or 3)

## Known Limitations

- Does not process subdirectories (only files in the specified folder)
- Overwrites existing .m4a files without confirmation
- Silence removal may cut audio that's intentionally quiet (music, ASMR, etc.)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Credits

Built with:
- [Python](https://www.python.org/)
- [FFmpeg](https://ffmpeg.org/)
- [PyInstaller](https://www.pyinstaller.org/)

## Support

For issues or feature requests, please open an issue on GitHub.

---

Made with ❤️ for passive learning enthusiasts
