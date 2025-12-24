# Video to Audio Converter

Batch-convert video files to .m4a audio format for passive listening. Useful for extracting audio from lectures, tutorials, and other educational content.

## Features

- **Batch Processing**: Convert all videos in a directory at once
- **Format Support**: .mp4, .mov, .avi, .mkv, .webm, and 15+ other formats
- **Audio Processing**:
  - Silence removal using FFmpeg or ML-based speech detection (TEN VAD)
  - Audio normalization to -16 LUFS for consistent volume
  - Multi-track audio selection
- **Standalone**: Pre-bundled executable with all dependencies (no installation required)

## Quick Start

### For End Users

1. Download the latest executable from releases
2. Run from command line or provide directory as argument:
   ```
   video-to-audio.exe
   video-to-audio.exe "C:\path\to\videos"
   ```
3. Configure processing options:
   - Silence removal (FFmpeg or ML-based speech detection)
   - Audio normalization
   - Audio track selection
4. Output files (.m4a) are saved alongside source videos with `_audio` suffix

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
  Use experimental machine learning for speech detection? (y/n): y
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

## Output

- **Format**: AAC audio, .m4a container, 160kbps
- **Location**: Same folder as source videos
- **Naming**: `video.mp4` → `video_audio.m4a`
- Existing files are overwritten

## Processing Options

### Silence Removal

Removes quiet sections (below -55dB for >1.2 seconds):
- **FFmpeg method**: Fast, reliable, threshold-based
- **TEN VAD ML method**: More accurate speech detection with 1-second buffer

### Audio Normalization

Adjusts loudness to -16 LUFS for consistent volume across files. Applied after silence removal.

### Audio Track Selection

Choose which audio track to extract (useful for multi-language videos or commentary tracks).

## System Requirements

- Windows 10+ (64-bit), macOS 10.13+, or Linux
- Disk space: ~150-600MB for executable (depending on ML support) + output files
- All dependencies bundled in executable

## Supported Formats

.mp4, .mov, .avi, .mkv, .webm, .flv, .wmv, .m4v, .mpg, .mpeg, .3gp, .ogv, .ts, .mts, .m2ts, .vob, .divx, .f4v

## For Developers

### Run from Source

```bash
python video_to_audio_converter.py
```

Requires Python 3.8+ and FFmpeg.

### Build Executable

```bash
pip install pyinstaller
pyinstaller video_to_audio.spec
```

See BUILD_INSTRUCTIONS.md for details.

## Troubleshooting

- **No video files found**: Check directory path and supported formats
- **Directory not accessible**: Verify path and permissions; use quotes for paths with spaces
- **Conversion fails**: File may be corrupted or lack audio track; try different track number

## Limitations

- Only processes files in specified directory (not subdirectories)
- Overwrites existing .m4a files
- Silence removal may cut intentionally quiet audio

## License

MIT License
